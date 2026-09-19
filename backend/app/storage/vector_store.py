import json
import numpy as np
from pathlib import Path
from typing import List, Dict

DATA_DIR = Path(__file__).parent.parent.parent / 'data' / 'embeddings'

class VectorStore:
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.file_path = DATA_DIR / f"{workspace_id}.json"
        self.embeddings: List[List[float]] = []
        self.metadata: List[Dict] = []
        self._load()

    def _load(self):
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.embeddings = data.get('embeddings', [])
                self.metadata = data.get('metadata', [])

    def _save(self):
        with open(self.file_path, 'w') as f:
            json.dump({'embeddings': self.embeddings, 'metadata': self.metadata}, f)

    def add_embedding(self, chunk_id: str, embedding: List[float], metadata: Dict):
        metadata['chunk_id'] = chunk_id
        self.embeddings.append(embedding)
        self.metadata.append(metadata)
        self._save()

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        if not self.embeddings:
            return []
        
        query_vec = np.array(query_embedding)
        embed_matrix = np.array(self.embeddings)
        
        # Cosine similarity
        norm_query = np.linalg.norm(query_vec)
        norm_embeds = np.linalg.norm(embed_matrix, axis=1)
        similarities = np.dot(embed_matrix, query_vec) / (norm_embeds * norm_query)
        
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            res = self.metadata[idx].copy()
            res['score'] = float(similarities[idx])
            results.append(res)
            
        return results

    def delete_by_evidence(self, evidence_id: str):
        indices_to_keep = [i for i, meta in enumerate(self.metadata) if meta.get('evidence_id') != evidence_id]
        self.embeddings = [self.embeddings[i] for i in indices_to_keep]
        self.metadata = [self.metadata[i] for i in indices_to_keep]
        self._save()
