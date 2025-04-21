from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class TicketBase(BaseModel):
    channel: str
    channel_id: str
    user_id: str
    message: str
    raw_data: Optional[Dict[str, Any]] = None

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    category_id: Optional[int] = None
    priority: Optional[str] = None
    resolution: Optional[str] = None

class TicketInDB(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime
    status: str
    assigned_to: Optional[str] = None
    category_id: Optional[int] = None
    priority: str
    resolution: Optional[str] = None

    class Config:
        orm_mode = True

class TicketResponse(TicketInDB):
    pass