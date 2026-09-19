from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

class RelationshipType(str, Enum):
    MENTIONS = 'mentions'
    REFERS_TO = 'refers_to'
    SAME_PERSON = 'same_person'
    SAME_ORGANIZATION = 'same_organization'
    SAME_EVENT = 'same_event'
    SAME_DATE = 'same_date'
    SAME_TOPIC = 'same_topic'
    SUPPORTS = 'supports'
    CONTRADICTS = 'contradicts'
    BEFORE = 'before'
    AFTER = 'after'
    RELATED_TO = 'related_to'

class Relationship(BaseModel):
    id: str
    workspace_id: str
    source_evidence_id: str
    target_evidence_id: str
    relationship: RelationshipType
    confidence: float
    reason: str
    supporting_text: List[str] = []
    created_at: datetime
    is_manual: bool = False
