import base64
import os
import zipfile

import pytest

from pyrannosaurus.utils import zip_to_binary, binary_to_zip, array_to_soql_string

def test_zip_to_binary():
    test_file = open('test.txt', 'w')
    test_file.write('testing')
    test_file.close()
    zipped = zipfile.ZipFile('test.zip', 'w')
    zipped.write('test.txt')
    zipped.close()

    enc_file = zip_to_binary('test.zip')

    assert enc_file

def test_binary_to_zip():
    test_file = open('test.txt', 'w')
    test_file.write('testing')
    test_file.close()
    zipped = zipfile.ZipFile('test.zip', 'w')
    zipped.write('test.txt')
    zipped.close()
    zipped = open('test.zip', 'r')
    zip_contents = zipped.read()
    zip_contents+="==="
    encoded_file = base64.b64encode(zip_contents)
    zipped.close()

    binary_to_zip(zip_contents)

    assert os.path.isfile('test.zip')

def test_zip_to_binary_and_back():
    package_file = open('tests/resources/zip_binary.txt')
    zip_contents = package_file.read().replace("\n", "")
    zip_contents = zip_contents.replace('"', '')
    binary_to_zip(zip_contents)
    return_binary = zip_to_binary('retrieve.zip')

    assert zip_contents == return_binary

def test_array_to_soql_string_str():
    ''' Test converting a string array to a soql usable array of string '''
    arr = ['1', '2', '3']
    soql_arr = array_to_soql_string(arr)
    assert soql_arr == "('1', '2', '3')"

def test_array_to_soql_string_int():
    ''' Test converting a string array to a soql usable array of ints'''
    arr = [1, 2, 3]
    soql_arr = array_to_soql_string(arr)
    assert soql_arr == "(1, 2, 3)"