from pathlib import Path
from adr_creator import get_next_adr_number

def test_next_number_empty_dir(tmp_path: Path):
    assert get_next_adr_number(tmp_path) == 1

def test_next_number_basic(tmp_path: Path):
    (tmp_path / "0001-test.md").touch()
    (tmp_path / "0002-test.md").touch()
    assert get_next_adr_number(tmp_path) == 3

def test_next_number_ignores_invalid_files(tmp_path: Path):
    (tmp_path / "abcd-test.md").touch()
    (tmp_path / "99999-test.md").touch()  # out of range
    (tmp_path / "0003-test.txt").touch()  # wrong extension

    assert get_next_adr_number(tmp_path) == 1

def test_next_number_sparse(tmp_path: Path):
    (tmp_path / "0005-test.md").touch()
    (tmp_path / "0010-test.md").touch()

    assert get_next_adr_number(tmp_path) == 11

def test_next_number_mixed_valid_invalid(tmp_path: Path):
    (tmp_path / "0001-test.md").touch()
    (tmp_path / "not-an-adr.md").touch()
    (tmp_path / "0002-something.md").touch()

    assert get_next_adr_number(tmp_path) == 3