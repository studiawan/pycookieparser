import json
import csv
import argparse
import os
from struct import unpack
from time import strftime, gmtime
from collections import Counter


class PyCookieParser(object):
    """
    A parser for binary cookie files.

    This class reads iOS binary cookie files and extracts cookie data
    including name, value, domain (URL), path, expiry date, creation date,
    and cookie flags (Secure, HttpOnly).

    The parser supports context manager usage for safe file handling::

        with PyCookieParser('cookies.binarycookies') as parser:
            cookies = parser.read_cookie_file()

    :param file_name: The name of the cookie file.
    :type file_name: str
    """
    
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.cookie_file = None
        self.offset = 0

    def __enter__(self):
        """
        Enter the context manager. Opens the cookie file.

        :return: The PyCookieParser instance.
        :rtype: PyCookieParser
        """
        self.open_file()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager. Closes the cookie file.

        :param exc_type: Exception type, if any.
        :param exc_val: Exception value, if any.
        :param exc_tb: Exception traceback, if any.
        :return: False (do not suppress exceptions).
        :rtype: bool
        """
        self.close_file()
        return False

    def open_file(self):
        """
        Open the cookie file for reading.
        If an IOError is encountered, a message is printed to the console.
        """
        
        try:
            self.cookie_file = open(self.file_name, 'rb')
        except IOError:
            print('Failed to open the cookie file:', self.file_name)

    def close_file(self):
        """
        Close the cookie file.
        This method checks if the cookie file is open before attempting to close it.
        """
        
        if self.cookie_file:
            self.cookie_file.close()
            self.cookie_file = None

    def read_cookie_file(self, silent: bool = False):
        """
        Read and parse the contents of the cookie file.
        Returns a list of cookies if successful, otherwise returns None.
        Each cookie is a dictionary with the following keys: 
        name, value, url, path, expiry_date, create_date, and cookie_flag.

        :param silent: If True, suppress warning messages for invalid files.
        :type silent: bool

        :return: A list of cookie dictionaries, or None on failure.
        :rtype: list or None
        """
        
        if not self.cookie_file:
            if not silent:
                print('No file opened.')
            return None

        try:
            file_header = self._read_chunk()
            if file_header != b'cook':
                if not silent:
                    print(self.file_name, 'is not a binary cookie file.')
                return None

            num_pages = self._read_chunk_big_endian()

            page_sizes = self._read_page_sizes(num_pages)

            cookies = self._read_cookies(page_sizes)

            return cookies

        except Exception:
            if not silent:
                print('Failed to read the cookie file:', self.file_name)
            return None

    def write_results(self, cookies: list, output_type: str, output_path: str, input_file: str) -> None:
        """
        Write parsed cookie results to a file.

        :param cookies: The list of parsed cookies.
        :type cookies: list
        :param output_type: The output format ('json', 'csv', or 'txt').
        :type output_type: str
        :param output_path: The directory path to write the output file.
        :type output_path: str
        :param input_file: The name of the input file (used to generate output filename).
        :type input_file: str
        """
        file_name = os.path.join(output_path, input_file + '-parsed') 
        parent_dir = os.path.dirname(file_name)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        
        if output_type == 'json':
            with open(file_name + '.json', 'w') as f:
                json.dump(cookies, f, indent=4)

        elif output_type == 'txt':
            with open(file_name + '.txt', 'w') as f:
                for cookie in cookies:
                    cookie_string = (
                        f"Cookie: {cookie['name']}={cookie['value']}; "
                        f"domain={cookie['url']}; "
                        f"path={cookie['path']}; "
                        f"created={cookie['create_date']};"
                        f"expires={cookie['expiry_date']}; "
                        f"{cookie['cookie_flag']}"
                    )
                    f.write(cookie_string + '\n')
        
        elif output_type == 'csv':
            with open(file_name + '.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 
                                 'value', 
                                 'url', 
                                 'path', 
                                 'expiry_date', 
                                 'create_date', 
                                 'cookie_flag'])

                for cookie in cookies:
                    row = [
                        cookie['name'], 
                        cookie['value'],
                        cookie['url'],
                        cookie['path'],
                        cookie['expiry_date'],
                        cookie['create_date'],
                        cookie['cookie_flag']
                    ]
                    writer.writerow(row)
        
        else:
            print('Output file type is not supported.')

    @staticmethod
    def summarize_cookies(cookies: list) -> dict:
        """
        Generate a statistical summary of parsed cookies.

        Produces a summary containing:
        - Total number of cookies
        - Number of unique domains
        - Cookie flag distribution
        - Top domains by cookie count

        :param cookies: The list of parsed cookies.
        :type cookies: list

        :return: A dictionary containing summary statistics.
        :rtype: dict
        """
        if not cookies:
            return {
                'total_cookies': 0,
                'unique_domains': 0,
                'flag_distribution': {},
                'top_domains': []
            }

        domains = [cookie.get('url', '') for cookie in cookies]
        flags = [cookie.get('cookie_flag', '') for cookie in cookies]

        domain_counts = Counter(domains)
        flag_counts = Counter(flags)

        top_domains = domain_counts.most_common(10)

        return {
            'total_cookies': len(cookies),
            'unique_domains': len(set(domains)),
            'flag_distribution': dict(flag_counts),
            'top_domains': top_domains
        }

    @staticmethod
    def batch_process(directory: str) -> dict:
        """
        Process all binary cookie files in a directory and its subdirectories.

        Scans the given directory recursively for files and attempts to parse each one
        as a binary cookie file. Files that are not valid binary cookie files
        are silently skipped.

        :param directory: The path to the directory containing cookie files.
        :type directory: str

        :return: A dictionary mapping relative file paths to their list of parsed cookies.
        :rtype: dict
        """
        results = {}

        if not os.path.isdir(directory):
            print(f"Directory not found: {directory}")
            return results

        for root, _, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(file_path, directory)

                try:
                    with PyCookieParser(file_path) as parser:
                        cookies = parser.read_cookie_file(silent=True)
                        if cookies is not None:
                            results[rel_path] = cookies
                except Exception:
                    # Skip files that cannot be parsed
                    continue

        return results
    
    def _increment_offset(self, chunk_size: int):
        """
        Increment the current offset into the cookie file by the given chunk size.
        
        :param chunk_size: The size of the chunk to increment by.
        :type chunk_size: int
        """
        
        self.offset += chunk_size
    
    def _read_chunk(self, chunk_size: int=4):
        """
        Read a chunk from the cookie file, incrementing the offset.
        Returns the chunk as a string of bytes.

        :param chunk_size: The size of the chunk to read.
        :type chunk_size: int
        """
        
        self.cookie_file.seek(self.offset)
        chunk = self.cookie_file.read(chunk_size)
        self._increment_offset(chunk_size)

        return chunk
    
    def _read_chunk_big_endian(self, chunk_size: int=4) -> int:
        """
        Read a chunk from the cookie file as a big-endian integer, incrementing the offset.
        Returns the chunk as an integer.

        :param chunk_size: The size of the chunk to read.
        :type chunk_size: int
        """
        
        self.cookie_file.seek(self.offset)
        chunk = unpack('>i', self.cookie_file.read(chunk_size))[0] 
        self._increment_offset(chunk_size)

        return chunk
    
    def _read_chunk_little_endian(self, chunk_size: int=4) -> int:
        """
        Read a chunk from the cookie file as a little-endian integer, incrementing the offset.
        Returns the chunk as an integer.

        :param chunk_size: The size of the chunk to read.
        :type chunk_size: int
        """
        
        self.cookie_file.seek(self.offset)
        chunk = unpack('<i', self.cookie_file.read(chunk_size))[0]
        self._increment_offset(chunk_size)

        return chunk
    
    def _read_chunk_double(self, chunk_size: int=8):
        """
        Read a chunk from the cookie file as a double precision float, incrementing the offset.
        Returns the chunk as a float.

        :param chunk_size: The size of the chunk to read.
        :type chunk_size: int
        """
        
        self.cookie_file.seek(self.offset)
        chunk = unpack('<d', self.cookie_file.read(chunk_size))[0]
        self._increment_offset(chunk_size)

        return chunk

    def _read_page_sizes(self, num_pages: int) -> list:
        """
        Read the sizes of all pages in the cookie file.

        :param num_pages: The number of pages to read.
        :type num_pages: int

        :return: List of page sizes.
        :rtype: list
        """
        
        page_sizes = []
        for page in range(num_pages):            
            page_size = self._read_chunk_big_endian()
            page_sizes.append(page_size)
        
        return page_sizes

    def _read_cookies(self, page_sizes: list) -> list:
        """
        Read all cookies from the cookie file.

        :param page_sizes: The sizes of the pages to read from.
        :type page_sizes: list

        :return: List of cookies. Each cookie is a dictionary.
        :rtype: list
        """
        
        cookies = []
        for _ in page_sizes:
            # header b'\x00\x00\x01\x00'
            _ = self._read_chunk()  

            # cookie number
            cookie_number = self._read_chunk_little_endian()

            cookie_offsets = self._read_cookie_offsets(cookie_number)

            # end of header b'\x00\x00\x00\x00'
            _ = self._read_chunk()

            for offset in cookie_offsets:
                cookie = self._read_cookie(offset)
                cookies.append(cookie)
        
        return cookies

    def _read_cookie_offsets(self, cookie_number: int) -> list:
        """
        Read the offsets for all cookies in a page.

        :param cookie_number: The number of cookies to read.
        :type cookie_number: int

        :return: List of cookie offsets.
        :rtype: list
        """
        
        cookie_offsets = []
        for _ in range(cookie_number):
            offset = self._read_chunk_little_endian()
            cookie_offsets.append(offset)
        
        return cookie_offsets

    def _read_cookie(self, offset: int) -> dict:
        """
        Read a cookie at a given offset in the cookie file.

        :param offset: The offset to read the cookie from.
        :type offset: int

        :return: A cookie. The cookie is a dictionary.
        :rtype: dict
        """
        
        cookie_size = self._read_chunk_little_endian()

        # unknown b'\x00\x00\x00\x00'
        _ = self._read_chunk()

        flag = self._read_chunk_little_endian()
        cookie_flag = self._get_cookie_flag(flag)

        # unknown b'\x00\x00\x00\x00'
        _ = self._read_chunk()

        urloffset = self._read_chunk_little_endian()
        nameoffset = self._read_chunk_little_endian()
        pathoffset = self._read_chunk_little_endian()
        valueoffset = self._read_chunk_little_endian()

        # unknown b'\x00\x00\x00\x00\x00\x00\x00\x00'
        _ = self._read_chunk(chunk_size=8)

        expiry_date_epoch = self._read_chunk_double() + 978307200
        expiry_date = strftime("%a, %d %b %Y ", gmtime(expiry_date_epoch))[:-1]

        create_date_epoch = self._read_chunk_double() + 978307200
        create_date = strftime("%a, %d %b %Y ", gmtime(create_date_epoch))[:-1]

        url = self._read_null_terminated_string()
        name = self._read_null_terminated_string()
        path = self._read_null_terminated_string()
        value = self._read_null_terminated_string()

        cookie = {
            'name': name,
            'value': value,
            'url': url,
            'path': path,
            'expiry_date': expiry_date,
            'create_date': create_date,
            'cookie_flag': cookie_flag
        }

        return cookie

    def _read_null_terminated_string(self, chunk_size=1) -> str:
        """
        Read a null-terminated string from the cookie file.

        :param chunk_size: The size of the chunk to read.
        :type chunk_size: int

        :return: A null-terminated string.
        :rtype: str
        """
        
        string = ''
        char = self.cookie_file.read(chunk_size)
        self._increment_offset(chunk_size)
        while unpack('<b', char)[0] != 0:
            string += char.decode('utf-8')
            char = self.cookie_file.read(chunk_size)
            self._increment_offset(chunk_size)
        
        return string

    def _get_cookie_flag(self, flag: int) -> str:
        """
        Determine the cookie flag.

        :param flag: The flag to determine.
        :type flag: int

        :return: The cookie flag as a string. If the flag is not recognized, returns 'Unknown'.
        :rtype: str
        """
        
        if flag == 0:
            return ''
        elif flag == 1:
            return 'Secure'
        elif flag == 4:
            return 'HttpOnly'
        elif flag == 5:
            return 'Secure; HttpOnly'
        else:
            return 'Unknown'


def main():
    # command option
    parser = argparse.ArgumentParser(description='iOS binary cookie parser.')
    parser.add_argument('-i', '--input_path', action='store', help='Input file path')
    parser.add_argument('-d', '--directory', action='store', help='Input directory path for batch processing')
    parser.add_argument('-t', '--output_type', choices=['txt', 'json', 'csv'], action='store', required=True, help='Output file type, such as txt, json, and csv')
    parser.add_argument('-o', '--output_path', action='store', required=True, help='Output file path')
    parser.add_argument('--summary', action='store_true', help='Print a statistical summary of parsed cookies')

    # parse arguments
    arguments = parser.parse_args()

    # validate: either input_path or directory must be provided
    if not arguments.input_path and not arguments.directory:
        parser.error('Either -i/--input_path or -d/--directory is required.')

    if arguments.input_path and arguments.directory:
        parser.error('Cannot use both -i/--input_path and -d/--directory at the same time.')

    # batch processing mode
    if arguments.directory:
        print('Batch processing directory:', arguments.directory)
        results = PyCookieParser.batch_process(arguments.directory)

        if not results:
            print('No valid cookie files found in the directory.')
            return

        all_cookies = []
        for file_name, cookies in results.items():
            print(f'  Parsed: {file_name} ({len(cookies)} cookies)')
            cookie_parser = PyCookieParser(os.path.join(arguments.directory, file_name))
            cookie_parser.write_results(cookies, arguments.output_type, arguments.output_path, file_name)
            all_cookies.extend(cookies)

        if arguments.summary and all_cookies:
            summary = PyCookieParser.summarize_cookies(all_cookies)
            _print_summary(summary)

        return

    # single file mode
    cookie_parser = PyCookieParser(arguments.input_path)
    print('Parsing a cookie file    :', arguments.input_path)
    cookie_parser.open_file()
    cookies = cookie_parser.read_cookie_file()
    cookie_parser.close_file()

    # get cookie file name
    file_name = os.path.basename(arguments.input_path)
    
    # write results
    if cookies:
        cookie_parser.write_results(cookies, arguments.output_type, arguments.output_path, file_name)
        print('Saving parsing results to:', os.path.join(arguments.output_path, file_name + '-parsed.' + arguments.output_type))

        if arguments.summary:
            summary = PyCookieParser.summarize_cookies(cookies)
            _print_summary(summary)


def _print_summary(summary: dict) -> None:
    """
    Print a formatted cookie summary to the console.

    :param summary: The summary dictionary from summarize_cookies.
    :type summary: dict
    """
    print('\n--- Cookie Summary ---')
    print(f"Total cookies      : {summary['total_cookies']}")
    print(f"Unique domains     : {summary['unique_domains']}")
    print(f"Flag distribution  : {summary['flag_distribution']}")
    print('Top domains:')
    for domain, count in summary['top_domains']:
        print(f"  {domain}: {count}")
    print('----------------------')


if __name__ == '__main__':
    main()
