# models/finance.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from ..database import Base
from datetime import datetime

class FinanceEntry(Base):
    __tablename__ = "finance_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, index=True)  # Link to farmer from Auth service
    date = Column(DateTime, default=datetime.utcnow)
    type = Column(String, index=True)        # Income / Expense
    amount = Column(Float)
    description = Column(String)
    crop = Column(String, nullable=True)     # Optional: which crop/activity
    category = Column(String, nullable=True) # Seeds, Fertilizer, Labor, Harvest, etc.
