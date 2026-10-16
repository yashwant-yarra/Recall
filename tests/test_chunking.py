import string
import pytest
from recall.chunking import chunk_pages

def test_short_page():
    assert chunk_pages(["hello"]) == [(1, "hello")]

def test_overlap():
    text = (string.ascii_letters * 50)[:2500]
    chunks = chunk_pages([text])
    assert len(chunks) == 3
    assert all(len(c) <= 1000 for _, c in chunks)
    assert chunks[0][1][-150:] == chunks[1][1][:150]
    assert chunks[-1][1].endswith(text[-150:])

def test_exact_size_is_one_chunk():
    assert len(chunk_pages(["x" * 1000])) == 1

def test_blank_page_keeps_numbering():
    assert [p for p, _ in chunk_pages(["abc", "  ", "def"])] == [1, 3]

def test_bad_overlap():
    with pytest.raises(ValueError):
        chunk_pages(["abc"], size=1000, overlap=1000)
