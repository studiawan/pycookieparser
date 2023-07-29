import os
import pytest
from struct import pack
from time import time, gmtime, strftime
from tempfile import NamedTemporaryFile
from pycookieparser import PyCookieParser


@pytest.fixture
def create_binary_cookie_file():
    """
    Creates a temporary binary cookie file for testing.
    """
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'cook\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x0f\x00\x00\x00\x16\x00\x00\x00\x1e')
        f.write(pack('<i', int(time())))
        f.write(pack('<i', 4))  # Cookie offset
        f.write(b'\x00' * 8)    # End of cookie
        f.write(pack('<d', time() + 978307200))
        f.write(pack('<d', time() + 978307200))
        f.write(b'http://example.com\x00')
        f.write(b'cookie_name\x00')
        f.write(b'/example/path\x00')
        f.write(b'cookie_value\x00')
    return f.name


def test_read_cookie_file(create_binary_cookie_file):
    parser = PyCookieParser(create_binary_cookie_file)
    cookies = parser.read_cookie_file()
    assert len(cookies) == 1
    cookie = cookies[0]
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
    cookies = parser.read_cookie_file()
    assert cookies is None


def test_read_cookie_file_no_file_opened():
    parser = PyCookieParser("non_existent_file")
    cookies = parser.read_cookie_file()
    assert cookies is None


def test_get_cookie_flag():
    parser = PyCookieParser("non_existent_file")
    assert parser._get_cookie_flag(0) == ''
    assert parser._get_cookie_flag(1) == 'Secure'
    assert parser._get_cookie_flag(4) == 'HttpOnly'
    assert parser._get_cookie_flag(5) == 'Secure; HttpOnly'
    assert parser._get_cookie_flag(10) == 'Unknown'


def test_read_null_terminated_string():
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'hello\x00world\x00')
    parser = PyCookieParser(f.name)
    string = parser._read_null_terminated_string()
    assert string == 'hello'
    string = parser._read_null_terminated_string()
    assert string == 'world'
    os.remove(f.name)


def test_read_page_sizes():
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'cook\x00\x00\x00\x01\x00\x00\x00\x05\x00\x00\x00\x0f\x00\x00\x00\x16\x00\x00\x00\x1e')
    parser = PyCookieParser(f.name)
    page_sizes = parser._read_page_sizes(1)
    assert page_sizes == [5, 15, 22]
    os.remove(f.name)


def test_read_chunk():
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'chunkdata')
    parser = PyCookieParser(f.name)
    chunk = parser._read_chunk()
    assert chunk == b'chun'
    os.remove(f.name)


def test_read_chunk_big_endian():
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'\x00\x00\x00\x01\x00\x00\x00\x05')
    parser = PyCookieParser(f.name)
    chunk = parser._read_chunk_big_endian()
    assert chunk == 1
    os.remove(f.name)


def test_read_chunk_little_endian():
    with NamedTemporaryFile(delete=False) as f:
        f.write(b'\x01\x00\x00\x00\x05\x00\x00\x00')
    parser = PyCookieParser(f.name)
    chunk = parser._read_chunk_little_endian()
    assert chunk == 1
    os.remove(f.name)


def test_read_chunk_double():
    with NamedTemporaryFile(delete=False) as f:
        f.write(pack('<d', 1.23))
    parser = PyCookieParser(f.name)
    chunk = parser._read_chunk_double()
    assert chunk == 1.23
    os.remove(f.name)
