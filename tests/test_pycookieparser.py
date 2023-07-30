import os
import pytest
from struct import pack
from time import time, gmtime, strftime
from tempfile import NamedTemporaryFile
from io import BytesIO
from pycookieparser.pycookieparser import PyCookieParser


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
    cookies = parser.read_cookie_file()
    assert cookies is None
    os.remove(f.name)


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
    parser.open_file()
    string = parser._read_null_terminated_string()
    assert string == 'hello'
    string = parser._read_null_terminated_string()
    assert string == 'world'
    parser.close_file()
    os.remove(f.name)


def test_read_page_sizes():
    pass


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
