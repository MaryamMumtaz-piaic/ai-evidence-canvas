from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = ''
    openai_model: str = 'gpt-4.1-mini'
    openai_vision_model: str = 'gpt-4.1-mini'
    embedding_model: str = 'text-embedding-3-small'
    max_file_size_mb: int = 50
    max_chunk_size: int = 1000
    chunk_overlap: int = 200
    max_chunks_per_evidence: int = 50
    rag_top_k: int = 5
    relationship_confidence_threshold: float = 0.7
    data_dir: str = '../data'
    
    class Config:
        env_file = '.env'
        
settings = Settings()
