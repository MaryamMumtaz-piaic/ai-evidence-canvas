import logging
import re
from typing import Dict, Any
import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader
from io import BytesIO

logger = logging.getLogger(__name__)

async def extract_from_pdf(file_path: str) -> dict:
    """Extract text from PDF using pypdf"""
    try:
        reader = PdfReader(file_path)
        text = ""
        pages = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            text += page_text + "\n"
            pages.append({"page_num": i + 1, "text": page_text})
            
        metadata = {
            "author": reader.metadata.author if reader.metadata else None,
            "title": reader.metadata.title if reader.metadata else None,
            "pages_count": len(reader.pages)
        }
        return {"text": text.strip(), "pages": pages, "metadata": metadata}
    except Exception as e:
        logger.error(f"Error extracting from PDF {file_path}: {e}")
        return {"text": "", "pages": [], "metadata": {}}

async def extract_from_image(file_path: str) -> dict:
    """Extract text/analysis from image using vision AI"""
    import base64
    from app.services.ai import analyze_image
    try:
        with open(file_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
        result = await analyze_image(img_b64)
        return {
            "text": result.get("text_found", ""),
            "description": result.get("description", ""),
            "entities": result.get("entities", []),
            "topics": result.get("topics", [])
        }
    except Exception as e:
        logger.error(f"Error extracting from image {file_path}: {e}")
        return {"text": "", "description": "", "entities": [], "topics": []}

async def extract_from_url(url: str) -> dict:
    """Fetch URL and extract readable content"""
    import datetime
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove nav, footer, ads, scripts
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        title = soup.title.string if soup.title else ""
        description = ""
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc:
            description = meta_desc.get("content", "")
            
        return {
            "text": text,
            "title": title,
            "description": description,
            "url": url,
            "fetched_at": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return {"text": "", "title": "", "description": "", "url": url, "fetched_at": ""}

async def extract_from_text(content: str, filename: str) -> dict:
    """Process plain text/markdown"""
    return {
        "text": content,
        "word_count": len(content.split()),
        "char_count": len(content)
    }

async def extract_from_email(content: str) -> dict:
    """Parse email content"""
    import email
    try:
        msg = email.message_from_string(content)
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore')
            
        return {
            "sender": msg.get("From", ""),
            "recipient": msg.get("To", ""),
            "subject": msg.get("Subject", ""),
            "date": msg.get("Date", ""),
            "body": body,
            "text": f"Subject: {msg.get('Subject', '')}\nFrom: {msg.get('From', '')}\nTo: {msg.get('To', '')}\nDate: {msg.get('Date', '')}\n\n{body}"
        }
    except Exception as e:
        logger.error(f"Error extracting email: {e}")
        return {"sender": "", "recipient": "", "subject": "", "date": "", "body": content, "text": content}

def sanitize_html(html: str) -> str:
    """Remove dangerous HTML, keep only text content"""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)
