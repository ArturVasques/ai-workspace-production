"""Unit tests for deterministic document chunking."""

import pytest

from app.services.rag.chunking import chunk_text


def test_short_text_produces_single_chunk() -> None:
    result = chunk_text("Recovery guidelines for athletes.")

    assert result == ["Recovery guidelines for athletes."]


def test_long_text_is_split_into_bounded_chunks() -> None:
    text = "word " * 1000

    result = chunk_text(
        text,
        chunk_size=200,
        overlap=40,
    )

    assert len(result) > 1
    assert all(len(chunk) <= 200 for chunk in result)


def test_empty_text_produces_no_chunks() -> None:
    assert chunk_text("   \n\n   ") == []


def test_invalid_overlap_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="overlap must be smaller than chunk_size",
    ):
        chunk_text(
            "content",
            chunk_size=100,
            overlap=100,
        )