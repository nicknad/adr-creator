from adr_creator import slugify, get_next_adr_number, build_adr_content

def test_slugify():
    assert slugify("Hello World") == "hello-world"
    assert slugify("HTMX for Active Web Pages!") == "htmx-for-active-web-pages"
    assert slugify("") == "untitled"
    assert slugify("Ä Ö Ü Test") == "a-o-u-test"

def test_next_number(tmp_path):
    (tmp_path / "0005-test.md").touch()
    (tmp_path / "0010-test.md").touch()

    assert get_next_adr_number(tmp_path) == 11

def test_build_content():
    content = build_adr_content(
        1, "Title", "Author", "proposed", "", "", "", "2025-01-01"
    )
    assert "No detailed context provided." in content