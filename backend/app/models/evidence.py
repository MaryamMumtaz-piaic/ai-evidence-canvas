from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class EvidenceType(str, Enum):
    PDF = 'pdf'
    IMAGE = 'image'
    URL = 'url'
    NOTE = 'note'
    EMAIL = 'email'
    TEXT = 'text'

class ProcessingStatus(str, Enum):
    UPLOADING = 'uploading'
    PROCESSING = 'processing'
    ANALYZING = 'analyzing'
    FINDING_RELATIONSHIPS = 'finding_relationships'
    READY = 'ready'
    FAILED = 'failed'

class EvidenceQuality(BaseModel):
    text_extracted: bool = False
    entities_found: bool = False
    dates_found: bool = False
    relationships_found: bool = False
    embedding_created: bool = False
    error_message: Optional[str] = None

class Evidence(BaseModel):
    id: str
    workspace_id: str
    type: EvidenceType
    title: str
    source_name: str
    source_url: Optional[str] = None
    file_path: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    entities: List[dict] = []
    topics: List[str] = []
    events: List[dict] = []
    claims: List[str] = []
    dates_found: List[str] = []
    chunks: List[str] = []
    embedding_ids: List[str] = []
    status: ProcessingStatus
    quality: EvidenceQuality
    canvas_position: dict = {}
    created_at: datetime
    updated_at: datetime
    metadata: dict = {}
