import pytest
from wmcontroller.myprog import hello

# def test_hello():
#     assert hello('World') == "Hello, World!"
#
#
# def test_hello_empty():
#     assert hello('') == "Hello, !"
#
#
# def test_hello_int():
#     assert hello(5) == "Hello, 5!"

@pytest.mark.parametrize('input_value, output_value',
                         [('world', 'Hello, world!'),
                          ('', 'Hello, !'),
                          ('5', 'Hello, 5!')])
def test_hello(input_value, output_value):
    assert hello(input_value) == output_value
