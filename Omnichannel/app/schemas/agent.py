from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class AgentBase(BaseModel):
    user_id: str
    name: str
    email: str
    is_active: bool = True

class AgentCreate(AgentBase):
    password: str

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    skills: Optional[List[int]] = None

class AgentInDB(AgentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    skills: List[int] = Field(default_factory=list)

    class Config:
        orm_mode = True

class AgentResponse(AgentInDB):
    pass