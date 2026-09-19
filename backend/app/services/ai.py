import json
import logging
from typing import List, Dict, Any, Optional
import openai
from pydantic import BaseModel, Field

from app.config import settings

logger = logging.getLogger(__name__)

client = openai.AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

class Entity(BaseModel):
    name: str
    type: str = Field(description="person, organization, product, location, date, contract, event, topic")

class Event(BaseModel):
    description: str
    date: str

class ExtractionResult(BaseModel):
    entities: List[Entity] = []
    topics: List[str] = []
    events: List[Event] = []
    claims: List[str] = []
    dates: List[str] = []

class Relationship(BaseModel):
    source_id: str
    target_id: str
    relationship: str
    confidence: float
    reason: str
    supporting_text: str

class RelationshipList(BaseModel):
    relationships: List[Relationship] = []

class InvestigationSummary(BaseModel):
    summary: str
    main_findings: List[str]
    important_entities: List[str]
    key_dates: List[str]
    contradictions: List[str]
    open_questions: List[str]

class AnswerSource(BaseModel):
    evidence_id: str
    source_name: str
    page: Optional[str] = None
    excerpt: str

class AnswerResult(BaseModel):
    answer: str
    sources: List[AnswerSource] = []
    confidence: float

async def summarize_evidence(text: str, evidence_type: str) -> str:
    """Generate a concise summary of evidence content"""
    if not client: return "Summary not available (OpenAI API key missing)."
    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": f"You are a helpful assistant. Summarize the following {evidence_type} in 2-3 sentences."},
                {"role": "user", "content": text[:10000]}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        logger.error(f"Error summarizing evidence: {e}")
        return ""

async def extract_entities_and_topics(text: str) -> dict:
    """Extract entities, topics, events, claims, dates from text"""
    if not client: return ExtractionResult().model_dump()
    try:
        response = await client.beta.chat.completions.parse(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "Extract entities, topics, events, claims, and dates from the provided text."},
                {"role": "user", "content": text[:20000]}
            ],
            response_format=ExtractionResult
        )
        return response.choices[0].message.parsed.model_dump()
    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        return ExtractionResult().model_dump()

async def analyze_image(image_base64: str) -> dict:
    """Analyze image using vision model"""
    if not client: return {"description": "", "entities": [], "topics": [], "text_found": ""}
    try:
        response = await client.chat.completions.create(
            model=settings.openai_vision_model,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "Describe this image and extract any entities, topics, and text found. Format as JSON with keys: description, entities, topics, text_found."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]}
            ],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content) if content else {}
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        return {}

async def detect_relationships(evidence_list: list) -> list:
    """Given a list of evidence items (with summary, entities, topics), detect relationships"""
    if not client: return []
    try:
        prompt = "Analyze the following evidence items and detect relationships between them. Output JSON matching the requested schema.\n"
        prompt += json.dumps(evidence_list, indent=2)
        
        response = await client.beta.chat.completions.parse(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are a relationship detector. Detect relationships between evidence items. Only return relationships with confidence > 0.7."},
                {"role": "user", "content": prompt}
            ],
            response_format=RelationshipList
        )
        relationships = response.choices[0].message.parsed.relationships
        return [r.model_dump() for r in relationships if r.confidence > settings.relationship_confidence_threshold]
    except Exception as e:
        logger.error(f"Error detecting relationships: {e}")
        return []

async def generate_investigation_summary(evidence_list: list, relationships: list) -> dict:
    """Generate overall investigation summary"""
    if not client: return InvestigationSummary(summary="", main_findings=[], important_entities=[], key_dates=[], contradictions=[], open_questions=[]).model_dump()
    try:
        data = {"evidence": evidence_list, "relationships": relationships}
        response = await client.beta.chat.completions.parse(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "Generate a comprehensive investigation summary based on the provided evidence and relationships."},
                {"role": "user", "content": json.dumps(data)[:50000]}
            ],
            response_format=InvestigationSummary
        )
        return response.choices[0].message.parsed.model_dump()
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return InvestigationSummary(summary="", main_findings=[], important_entities=[], key_dates=[], contradictions=[], open_questions=[]).model_dump()

async def answer_question(question: str, context_chunks: list) -> dict:
    """RAG Q&A - answer question given retrieved context chunks"""
    if not client: return AnswerResult(answer="Q&A not available.", confidence=0.0).model_dump()
    try:
        context_str = json.dumps(context_chunks, indent=2)
        response = await client.beta.chat.completions.parse(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are an AI assistant. Answer the user's question based strictly on the provided context chunks. If you cannot answer based on the context, state that clearly."},
                {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {question}"}
            ],
            response_format=AnswerResult
        )
        return response.choices[0].message.parsed.model_dump()
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return AnswerResult(answer="Error generating answer.", confidence=0.0).model_dump()
