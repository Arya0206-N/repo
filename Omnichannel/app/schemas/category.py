from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class CategoryInDB(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CategoryResponse(CategoryInDB):
    pass