import logging
from app.services.ai import detect_relationships
# from app.storage import db

logger = logging.getLogger(__name__)

async def find_relationships_for_evidence(new_evidence_id: str, workspace_id: str) -> list:
    """
    Find relationships between new evidence and all existing evidence.
    """
    # 1. Get new evidence (entities, topics, summary)
    # new_evidence = await db.get_evidence_with_metadata(new_evidence_id)
    new_evidence = {"id": new_evidence_id, "summary": "mock summary", "entities": [], "topics": []}
    
    # 2. Get all other evidence in workspace
    # existing_evidence = await db.get_all_evidence_in_workspace(workspace_id, exclude=new_evidence_id)
    existing_evidence = []
    
    if not existing_evidence:
        return []
        
    evidence_list = [new_evidence] + existing_evidence
    
    # 3. Call ai.detect_relationships() with pairs
    relationships = await detect_relationships(evidence_list)
    
    # 4. Save valid relationships to storage
    valid_relationships = [r for r in relationships if r.get('source_id') == new_evidence_id or r.get('target_id') == new_evidence_id]
    # await db.save_relationships(valid_relationships)
    
    # 5. Return list of new relationships
    return valid_relationships

async def find_all_relationships(workspace_id: str) -> list:
    """
    Re-analyze all evidence in workspace for relationships.
    Used when user triggers full analysis.
    """
    # evidence_list = await db.get_all_evidence_in_workspace(workspace_id)
    evidence_list = []
    if not evidence_list:
        return []
        
    relationships = await detect_relationships(evidence_list)
    # await db.clear_and_save_relationships(workspace_id, relationships)
    return relationships

async def get_graph_data(workspace_id: str) -> dict:
    """
    Build graph data for visualization.
    """
    # evidence_items = await db.get_all_evidence_in_workspace(workspace_id)
    # relationships = await db.get_relationships_for_workspace(workspace_id)
    # entities = await db.get_entities_for_workspace(workspace_id)
    
    nodes = []
    edges = []
    
    return {
        "nodes": nodes,
        "edges": edges
    }

async def extract_and_store_entities(evidence_id: str, workspace_id: str, entities: list):
    """Store extracted entities and link to evidence"""
    # await db.save_entities(workspace_id, entities)
    # await db.link_entities_to_evidence(evidence_id, [e.name for e in entities])
    pass
