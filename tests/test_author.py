import os
from adr_creator import default_author

def test_default_author_git(monkeypatch):
    monkeypatch.setenv("GIT_AUTHOR_NAME", "GitUser")
    monkeypatch.delenv("USERNAME", raising=False)
    monkeypatch.delenv("USER", raising=False)

    assert default_author() == "GitUser"

def test_default_author_username(monkeypatch):
    monkeypatch.delenv("GIT_AUTHOR_NAME", raising=False)
    monkeypatch.setenv("USERNAME", "WinUser")
    monkeypatch.delenv("USER", raising=False)

    assert default_author() == "WinUser"

def test_default_author_user(monkeypatch):
    monkeypatch.delenv("GIT_AUTHOR_NAME", raising=False)
    monkeypatch.delenv("USERNAME", raising=False)
    monkeypatch.setenv("USER", "UnixUser")

    assert default_author() == "UnixUser"

def test_default_author_fallback(monkeypatch):
    monkeypatch.delenv("GIT_AUTHOR_NAME", raising=False)
    monkeypatch.delenv("USERNAME", raising=False)
    monkeypatch.delenv("USER", raising=False)

    assert default_author() == "Unknown"