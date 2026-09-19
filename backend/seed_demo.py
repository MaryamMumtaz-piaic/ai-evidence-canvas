#!/usr/bin/env python3
"""
Seed demo data for AI Evidence Canvas.
Run: python seed_demo.py
"""
import json
import shutil
from pathlib import Path

DATA_DIR = Path(__file__).parent / 'data'

def seed():
    # Create all data directories
    for dir_name in ['workspaces', 'evidence', 'embeddings', 'relationships', 'timelines', 'exports', 'uploads']:
        (DATA_DIR / dir_name).mkdir(parents=True, exist_ok=True)
    
    # Load demo JSON files
    demo_dir = DATA_DIR / 'demo'
    
    # Copy workspace
    workspace = json.loads((demo_dir / 'workspace.json').read_text())
    (DATA_DIR / 'workspaces' / f"{workspace['id']}.json").write_text(json.dumps(workspace, indent=2))
    
    # Copy evidence items
    evidence_list = json.loads((demo_dir / 'evidence.json').read_text())
    index = []
    for ev in evidence_list:
        (DATA_DIR / 'evidence' / f"{ev['id']}.json").write_text(json.dumps(ev, indent=2))
        index.append({'id': ev['id'], 'workspace_id': ev['workspace_id'], 'type': ev['type'], 'title': ev['title']})
    (DATA_DIR / 'evidence' / 'index.json').write_text(json.dumps(index, indent=2))
    
    # Copy relationships
    relationships = json.loads((demo_dir / 'relationships.json').read_text())
    for rel in relationships:
        (DATA_DIR / 'relationships' / f"{rel['id']}.json").write_text(json.dumps(rel, indent=2))
    
    print(f'✓ Seeded workspace: {workspace["name"]}')
    print(f'✓ Seeded {len(evidence_list)} evidence items')
    print(f'✓ Seeded {len(relationships)} relationships')
    print('\nDemo data ready! Start the backend and open the app.')

if __name__ == '__main__':
    seed()
