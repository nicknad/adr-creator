from adr_creator import build_adr_content

def test_build_content_defaults():
    content = build_adr_content(
        1, "Title", "Author", "proposed", "", "", "", "2025-01-01"
    )

    assert "# 0001 - Title" in content
    assert "**Status:** Proposed" in content
    assert "**Date:** 2025-01-01" in content
    assert "**Author:** Author" in content

    assert "No detailed context provided." in content
    assert "No decision recorded yet." in content
    assert "No consequences recorded yet." in content

def test_build_content_custom_values():
    content = build_adr_content(
        42,
        "Scaling Strategy",
        "Nick",
        "accepted",
        "context",
        "decision",
        "impact",
        "2025-01-01",
    )

    assert "# 0042 - Scaling Strategy" in content
    assert "**Status:** Accepted" in content
    assert "context" in content
    assert "decision" in content
    assert "impact" in content

def test_build_content_format_stability():
    content = build_adr_content(
        7, "Test", "A", "proposed", "c", "d", "e", "2025-01-01"
    )

    # contract-like assertions
    assert content.count("## Context") == 1
    assert content.count("## Decision") == 1
    assert content.count("## Consequences") == 1