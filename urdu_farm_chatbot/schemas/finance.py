# schemas/finance.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FinanceEntryBase(BaseModel):
    type: str          # Income / Expense
    amount: float
    description: str
    crop: str | None = None
    category: str | None = None
    date: datetime | None = None

class FinanceEntryCreate(FinanceEntryBase):
    pass

class FinanceEntryUpdate(BaseModel):
    type: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    crop: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None

class FinanceEntryResponse(FinanceEntryBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True
