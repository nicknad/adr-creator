import pytest
from adr_creator import slugify

@pytest.mark.parametrize(
    "input,expected",
    [
        ("Hello World", "hello-world"),
        ("HTMX for Active Web Pages!", "htmx-for-active-web-pages"),
        ("", "untitled"),
        ("Ä Ö Ü Test", "a-o-u-test"),
        ("---Hello---World---", "hello-world"),
        ("   spaced   out   ", "spaced-out"),
        ("Symbols #$%^&*", "symbols"),
    ],
)
def test_slugify_basic(input, expected):
    assert slugify(input) == expected

def test_slugify_max_length():
    text = "a" * 200
    result = slugify(text)
    assert len(result) <= 100

def test_slugify_only_invalid_chars():
    assert slugify("!!!@@@###") == "untitled"

def test_slugify_unicode_normalization():
    assert slugify("éèê") == "eee"