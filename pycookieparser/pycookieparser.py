import json
import csv
import argparse
import os
from struct import unpack
from time import strftime, gmtime


class PyCookieParser(object):
    """
    A parser for binary cookie files.
    
    :param file_name: The name of the cookie file.
    :type file_name: str
    """
    
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.cookie_file = None
        self.offset = 0

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

    def read_cookie_file(self):
        """
        Read and parse the contents of the cookie file.
        Returns a list of cookies if successful, otherwise returns None.
        Each cookie is a dictionary with the following keys: 
        name, value, url, path, expiry_date, create_date, and cookie_flag.
        """
        
        if not self.cookie_file:
            print('No file opened.')
            return None

        try:
            file_header = self._read_chunk()
            if file_header != b'cook':
                print(self.file_name, 'is not a binary cookie file.')
                return None

            num_pages = self._read_chunk_big_endian()
            # print('Number of pages:', num_pages)

            page_sizes = self._read_page_sizes(num_pages)

            cookies = self._read_cookies(page_sizes)

            return cookies

        except IOError:
            print('Failed to read the cookie file:', self.file_name)
            return None

    def write_results(self, cookies: list, output_type: str, output_path: str, input_file: str) -> None:
        file_name = os.path.join(output_path, input_file + '-parsed') 
        
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
            
            # print('Page:', page, 'size:', page_size)
        
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
            # header
            _ = self._read_chunk()  

            # cookie number
            cookie_number = self._read_chunk_little_endian()
            # print('Cookie number:', cookie_number)

            cookie_offsets = self._read_cookie_offsets(cookie_number)

            # end of header
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

            # print('Cookie offset', offset)
        
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
        # print('Cookie size:', cookie_size)

        # unknown
        _ = self._read_chunk()

        flag = self._read_chunk_little_endian()
        cookie_flag = self._get_cookie_flag(flag)
        # print('Flag:', flag, cookie_flag)

        # unknown
        _ = self._read_chunk()

        urloffset = self._read_chunk_little_endian()
        nameoffset = self._read_chunk_little_endian()
        pathoffset = self._read_chunk_little_endian()
        valueoffset = self._read_chunk_little_endian()

        # print(urloffset, nameoffset, pathoffset, valueoffset)

        # end of cookie
        _ = self._read_chunk(chunk_size=8)

        expiry_date_epoch = self._read_chunk_double() + 978307200
        expiry_date = strftime("%a, %d %b %Y ", gmtime(expiry_date_epoch))[:-1]
        # print(expiry_date)

        create_date_epoch = self._read_chunk_double() + 978307200
        create_date = strftime("%a, %d %b %Y ", gmtime(create_date_epoch))[:-1]
        # print(create_date)

        url = self._read_null_terminated_string()
        name = self._read_null_terminated_string()
        path = self._read_null_terminated_string()
        value = self._read_null_terminated_string()
        # print(url, name, path, value)

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
    parser.add_argument('-i', '--input_path', action='store', required=True, help='Input file path')
    parser.add_argument('-t', '--output_type', choices=['txt', 'json', 'csv'], action='store', required=True, help='Output file type, such as txt, json, and csv')
    parser.add_argument('-o', '--output_path', action='store', required=True, help='Output file path')

    # parse arguments
    arguments = parser.parse_args()

    # call the parser
    parser = PyCookieParser(arguments.input_path)
    print('Parsing a cookie file    :', arguments.input_path)
    parser.open_file()
    cookies = parser.read_cookie_file()
    parser.close_file()

    # get cookie file name
    file_name = os.path.basename(arguments.input_path)
    
    # write results
    if cookies:
        parser.write_results(cookies, arguments.output_type, arguments.output_path, file_name)
        print('Saving parsing results to:', os.path.join(arguments.output_path, file_name + '-parsed.' + arguments.output_type))
