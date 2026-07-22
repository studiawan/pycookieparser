import os
import json
import csv
import pytest
from struct import pack
from time import time, gmtime, strftime
from tempfile import NamedTemporaryFile, TemporaryDirectory
from io import BytesIO
from pycookieparser.pycookieparser import PyCookieParser

# Test: Reading cookie file

def test_read_cookie_file():
    cookie_file = 'tests/fdda2f81cc0b838dc00e3050b14da7ef2d835f3c'
    parser = PyCookieParser(cookie_file)
    parser.open_file()
    cookies = parser.read_cookie_file()
    parser.close_file()
    
    cookie = cookies[0]
    assert len(cookies) == 12
    assert len(cookie) == 7
    assert isinstance(cookie, dict)
    assert 'name' in cookie
    assert 'value' in cookie
    assert 'url' in cookie
    assert 'path' in cookie
    assert 'expiry_date' in cookie
    assert 'create_date' in cookie
    assert 'cookie_flag' in cookie


def test_read_cookie_file_invalid_file():
    parser = PyCookieParser("non_existent_file")
    cookies = parser.read_cookie_file()
    assert cookies is None


def test_read_cookie_file_invalid_format():
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'invalid_data')
    parser = PyCookieParser(f.name)
    parser.open_file()
    cookies = parser.read_cookie_file()
    parser.close_file()
    assert cookies is None
    os.remove(f.name)


def test_read_cookie_file_no_file_opened():
    parser = PyCookieParser("some_file")
    # Deliberately do not call open_file()
    cookies = parser.read_cookie_file()
    assert cookies is None

# Test: Cookie flag

def test_get_cookie_flag():
    parser = PyCookieParser("non_existent_file")
    assert parser._get_cookie_flag(0) == ''
    assert parser._get_cookie_flag(1) == 'Secure'
    assert parser._get_cookie_flag(4) == 'HttpOnly'
    assert parser._get_cookie_flag(5) == 'Secure; HttpOnly'
    assert parser._get_cookie_flag(10) == 'Unknown'

# Test: Reading strings and chunks

def test_read_null_terminated_string():
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'hello\x00world\x00')
    
    parser = PyCookieParser(f.name)
    parser.open_file()
    string = parser._read_null_terminated_string()
    assert string == 'hello'
    string = parser._read_null_terminated_string()
    assert string == 'world'
    parser.close_file()
    os.remove(f.name)


def test_read_page_sizes():
    with NamedTemporaryFile(delete=False) as f:
        # Write 3 page sizes as big-endian integers
        f.write(pack('>i', 100))
        f.write(pack('>i', 200))
        f.write(pack('>i', 300))

    parser = PyCookieParser(f.name)
    parser.open_file()
    page_sizes = parser._read_page_sizes(3)
    parser.close_file()

    assert page_sizes == [100, 200, 300]
    assert len(page_sizes) == 3
    os.remove(f.name)


def test_read_chunk():
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'chunkdata')
    
    parser = PyCookieParser(f.name)
    parser.open_file()
    chunk = parser._read_chunk()
    parser.close_file()
    
    assert chunk == b'chun'
    os.remove(f.name)


def test_read_chunk_big_endian():
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'\x00\x00\x00\x01\x00\x00\x00\x05')
    
    parser = PyCookieParser(f.name)
    parser.open_file()
    chunk = parser._read_chunk_big_endian()
    parser.close_file()

    assert chunk == 1
    os.remove(f.name)


def test_read_chunk_little_endian():
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'\x01\x00\x00\x00\x05\x00\x00\x00')
    
    parser = PyCookieParser(f.name)
    parser.open_file()
    chunk = parser._read_chunk_little_endian()
    parser.close_file()

    assert chunk == 1
    os.remove(f.name)


def test_read_chunk_double():
    with NamedTemporaryFile(delete=False) as f:
        f.write(pack('<d', 1.23))
    
    parser = PyCookieParser(f.name)
    parser.open_file()
    chunk = parser._read_chunk_double()
    parser.close_file()

    assert chunk == 1.23
    os.remove(f.name)

# Test: File open/close errors

def test_open_file_ioerror(capsys):
    parser = PyCookieParser("/nonexistent/path/to/file")
    parser.open_file()

    captured = capsys.readouterr()
    assert 'Failed to open the cookie file' in captured.out
    assert parser.cookie_file is None

# Test: Write results

def _create_sample_cookies():
    """Helper to create sample cookie data for write tests."""
    return [
        {
            'name': 'session_id',
            'value': 'abc123',
            'url': '.example.com',
            'path': '/',
            'expiry_date': 'Mon, 01 Jan 2030',
            'create_date': 'Fri, 15 Jul 2026',
            'cookie_flag': 'Secure'
        },
        {
            'name': 'tracker',
            'value': 'xyz789',
            'url': '.tracker.com',
            'path': '/track',
            'expiry_date': 'Tue, 31 Dec 2030',
            'create_date': 'Fri, 15 Jul 2026',
            'cookie_flag': 'HttpOnly'
        }
    ]


def test_write_results_json():
    cookies = _create_sample_cookies()

    with TemporaryDirectory() as tmpdir:
        parser = PyCookieParser("dummy")
        parser.write_results(cookies, 'json', tmpdir, 'testfile')

        output_file = os.path.join(tmpdir, 'testfile-parsed.json')
        assert os.path.exists(output_file)

        with open(output_file, 'r') as f:
            loaded = json.load(f)

        assert len(loaded) == 2
        assert loaded[0]['name'] == 'session_id'
        assert loaded[1]['value'] == 'xyz789'


def test_write_results_csv():
    cookies = _create_sample_cookies()

    with TemporaryDirectory() as tmpdir:
        parser = PyCookieParser("dummy")
        parser.write_results(cookies, 'csv', tmpdir, 'testfile')

        output_file = os.path.join(tmpdir, 'testfile-parsed.csv')
        assert os.path.exists(output_file)

        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # header + 2 data rows
        assert len(rows) == 3
        assert rows[0] == ['name', 'value', 'url', 'path', 'expiry_date', 'create_date', 'cookie_flag']
        assert rows[1][0] == 'session_id'
        assert rows[2][0] == 'tracker'


def test_write_results_txt():
    cookies = _create_sample_cookies()

    with TemporaryDirectory() as tmpdir:
        parser = PyCookieParser("dummy")
        parser.write_results(cookies, 'txt', tmpdir, 'testfile')

        output_file = os.path.join(tmpdir, 'testfile-parsed.txt')
        assert os.path.exists(output_file)

        with open(output_file, 'r') as f:
            lines = f.readlines()

        assert len(lines) == 2
        assert 'session_id=abc123' in lines[0]
        assert 'domain=.example.com' in lines[0]
        assert 'tracker=xyz789' in lines[1]


def test_write_results_invalid_type(capsys):
    cookies = _create_sample_cookies()

    with TemporaryDirectory() as tmpdir:
        parser = PyCookieParser("dummy")
        parser.write_results(cookies, 'xml', tmpdir, 'testfile')

        captured = capsys.readouterr()
        assert 'Output file type is not supported' in captured.out

# Test: Context manager

def test_context_manager():
    cookie_file = 'tests/fdda2f81cc0b838dc00e3050b14da7ef2d835f3c'

    with PyCookieParser(cookie_file) as parser:
        assert parser.cookie_file is not None
        cookies = parser.read_cookie_file()
        assert cookies is not None
        assert len(cookies) == 12

    # After exiting context, file should be closed
    assert parser.cookie_file is None


def test_context_manager_invalid_file():
    with PyCookieParser("/nonexistent/file") as parser:
        assert parser.cookie_file is None
        cookies = parser.read_cookie_file()
        assert cookies is None

# Test: Summarize cookies

def test_summarize_cookies():
    cookies = _create_sample_cookies()
    summary = PyCookieParser.summarize_cookies(cookies)

    assert summary['total_cookies'] == 2
    assert summary['unique_domains'] == 2
    assert 'Secure' in summary['flag_distribution']
    assert 'HttpOnly' in summary['flag_distribution']
    assert summary['flag_distribution']['Secure'] == 1
    assert summary['flag_distribution']['HttpOnly'] == 1
    assert len(summary['top_domains']) == 2


def test_summarize_cookies_empty():
    summary = PyCookieParser.summarize_cookies([])

    assert summary['total_cookies'] == 0
    assert summary['unique_domains'] == 0
    assert summary['flag_distribution'] == {}
    assert summary['top_domains'] == []


def test_summarize_cookies_none():
    summary = PyCookieParser.summarize_cookies(None)

    assert summary['total_cookies'] == 0


def test_summarize_cookies_same_domain():
    cookies = [
        {'name': 'a', 'value': '1', 'url': '.example.com', 'path': '/', 'expiry_date': '', 'create_date': '', 'cookie_flag': 'Secure'},
        {'name': 'b', 'value': '2', 'url': '.example.com', 'path': '/', 'expiry_date': '', 'create_date': '', 'cookie_flag': 'Secure'},
        {'name': 'c', 'value': '3', 'url': '.other.com', 'path': '/', 'expiry_date': '', 'create_date': '', 'cookie_flag': ''},
    ]
    summary = PyCookieParser.summarize_cookies(cookies)

    assert summary['total_cookies'] == 3
    assert summary['unique_domains'] == 2
    # .example.com should be the top domain
    assert summary['top_domains'][0] == ('.example.com', 2)

# Test: Batch processing

def test_batch_processing():
    cookie_file_src = 'tests/fdda2f81cc0b838dc00e3050b14da7ef2d835f3c'

    with TemporaryDirectory() as tmpdir:
        # Copy the test cookie file into the temp directory
        import shutil
        dest = os.path.join(tmpdir, 'cookie_file_1')
        shutil.copy2(cookie_file_src, dest)

        results = PyCookieParser.batch_process(tmpdir)

        assert len(results) == 1
        assert 'cookie_file_1' in results
        assert len(results['cookie_file_1']) == 12


def test_batch_processing_empty_directory():
    with TemporaryDirectory() as tmpdir:
        results = PyCookieParser.batch_process(tmpdir)
        assert results == {}


def test_batch_processing_invalid_directory():
    results = PyCookieParser.batch_process('/nonexistent/directory')
    assert results == {}


def test_batch_processing_mixed_files(capsys):
    cookie_file_src = 'tests/fdda2f81cc0b838dc00e3050b14da7ef2d835f3c'

    with TemporaryDirectory() as tmpdir:
        # Copy valid cookie file
        import shutil
        shutil.copy2(cookie_file_src, os.path.join(tmpdir, 'valid_cookie'))

        # Create an invalid file
        with open(os.path.join(tmpdir, 'invalid_file.txt'), 'w') as f:
            f.write('this is not a cookie file')

        results = PyCookieParser.batch_process(tmpdir)

        # Only the valid cookie file should be in results
        assert 'valid_cookie' in results
        assert 'invalid_file.txt' not in results

        # Verify non-cookie file was silently skipped without output
        captured = capsys.readouterr()
        assert 'is not a binary cookie file' not in captured.out


def test_batch_processing_subdirectories():
    cookie_file_src = 'tests/fdda2f81cc0b838dc00e3050b14da7ef2d835f3c'

    with TemporaryDirectory() as tmpdir:
        import shutil
        subdir = os.path.join(tmpdir, 'subfolder')
        os.makedirs(subdir, exist_ok=True)

        shutil.copy2(cookie_file_src, os.path.join(subdir, 'nested_cookie'))

        results = PyCookieParser.batch_process(tmpdir)

        expected_key = os.path.join('subfolder', 'nested_cookie')
        assert expected_key in results
        assert len(results[expected_key]) == 12


def test_read_cookie_file_silent(capsys):
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'invalid_data')

    parser = PyCookieParser(f.name)
    parser.open_file()
    cookies = parser.read_cookie_file(silent=True)
    parser.close_file()

    assert cookies is None
    captured = capsys.readouterr()
    assert captured.out == ''
    os.remove(f.name)


def test_batch_processing_full_dataset():
    if not os.path.exists('dataset'):
        pytest.skip("dataset directory not found")

    results = PyCookieParser.batch_process('dataset')
    assert len(results) == 36
    total_cookies = sum(len(cookies) for cookies in results.values())
    assert total_cookies == 389


