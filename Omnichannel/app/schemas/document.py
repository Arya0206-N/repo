from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class DocumentBase(BaseModel):
    title: str
    source: str
    content: str
    metadata: Optional[dict] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[dict] = None

class DocumentInDB(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    embedding_id: Optional[str] = None

    class Config:
        orm_mode = True

class DocumentResponse(DocumentInDB):
    pass

class DocumentChunk(BaseModel):
    document_id: int
    chunk_text: str
    chunk_index: int
    embedding_id: Optional[str] = None

class DocumentSearchResult(BaseModel):
    document: DocumentResponse
    score: float
    chunks: List[DocumentChunk]