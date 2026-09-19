def validate_file(filename: str, size: int) -> bool:
    allowed_extensions = {".pdf", ".txt", ".md", ".json", ".csv"}
    import os
    _, ext = os.path.splitext(filename)
    if ext.lower() not in allowed_extensions:
        return False
    # 50MB limit
    if size > 50 * 1024 * 1024:
        return False
    return True

def validate_url(url: str) -> bool:
    from urllib.parse import urlparse
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except:
        return False

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i + chunk_size])
        i += chunk_size - overlap
    return chunks
