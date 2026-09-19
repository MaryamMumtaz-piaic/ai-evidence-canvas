import logging
import dateparser
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

async def build_timeline(workspace_id: str) -> list:
    """
    Extract all dates from evidence and build chronological timeline.
    """
    # evidence_list = await db.get_all_evidence_with_dates(workspace_id)
    evidence_list = []
    
    timeline_events = []
    for evidence in evidence_list:
        dates_list = evidence.get("dates", [])
        for date_str in dates_list:
            parsed = parse_date(date_str)
            if parsed:
                timeline_events.append({
                    "date": date_str,
                    "date_parsed": parsed,
                    "events": [
                        {
                            "evidence_id": evidence.get("id"),
                            "title": evidence.get("title", ""),
                            "description": evidence.get("summary", ""),
                            "evidence_type": evidence.get("type", "unknown")
                        }
                    ]
                })
                
    grouped = {}
    for item in timeline_events:
        ts = item["date_parsed"].timestamp()
        if ts not in grouped:
            grouped[ts] = item
        else:
            grouped[ts]["events"].extend(item["events"])
            
    sorted_events = sorted(grouped.values(), key=lambda x: x["date_parsed"])
    return sorted_events

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse various date formats"""
    try:
        parsed = dateparser.parse(date_str)
        return parsed
    except Exception as e:
        logger.warning(f"Failed to parse date string {date_str}: {e}")
        return None
