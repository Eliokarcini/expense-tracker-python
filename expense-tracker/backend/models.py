from pydantic import BaseModel
from typing import List, Optional

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category: str
    date: str

class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    date: str
    created_at: str

    class Config:
        from_attributes = True