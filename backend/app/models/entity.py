from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

class EntityType(str, Enum):
    PERSON = 'person'
    ORGANIZATION = 'organization'
    PRODUCT = 'product'
    LOCATION = 'location'
    DATE = 'date'
    IP_ADDRESS = 'ip_address'
    URL = 'url'
    CONTRACT = 'contract'
    EVENT = 'event'
    TOPIC = 'topic'

class Entity(BaseModel):
    id: str
    workspace_id: str
    name: str
    type: EntityType
    evidence_ids: List[str] = []
    created_at: datetime
