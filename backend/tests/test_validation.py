import pytest
from app.services.validation import validate_file, validate_url, chunk_text
# Assuming the validation logic will be in app.services.validation

def test_validate_valid_pdf_file():
    # Mock file validation
    assert validate_file("test.pdf", 1024) == True

def test_validate_invalid_extension():
    assert validate_file("test.exe", 1024) == False

def test_validate_oversized_file():
    # Assume max size is 50MB (50 * 1024 * 1024 bytes)
    assert validate_file("large.pdf", 60 * 1024 * 1024) == False

def test_validate_valid_url():
    assert validate_url("https://example.com") == True
    assert validate_url("http://example.com/path?q=1") == True

def test_validate_invalid_url_scheme():
    assert validate_url("ftp://example.com") == False

def test_validate_malformed_url():
    assert validate_url("not a url") == False

def test_chunk_text_basic():
    text = "Word " * 1000
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1

def test_chunk_text_overlap():
    text = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    chunks = chunk_text(text, chunk_size=10, overlap=5)
    # Just checking it chunks properly
    assert len(chunks) > 1
    # Check overlap logic if applicable
    assert "F G" in chunks[0] or "F G" in chunks[1]

def test_chunk_text_short_text():
    text = "Short text"
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) == 1
    assert chunks[0] == text
