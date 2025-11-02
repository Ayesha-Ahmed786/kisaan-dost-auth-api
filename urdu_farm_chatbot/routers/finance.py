# routers/finance.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import finance as finance_model
from ..schemas import finance as finance_schema

router = APIRouter()

# ----------------------
# Add a new transaction
# ----------------------
@router.post("/", response_model=finance_schema.FinanceEntryResponse)
def add_transaction(
    entry: finance_schema.FinanceEntryCreate,
    db: Session = Depends(get_db)
):
    transaction = finance_model.FinanceEntry(**entry.dict())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

# ----------------------
# Get all transactions
# ----------------------
@router.get("/", response_model=List[finance_schema.FinanceEntryResponse])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(finance_model.FinanceEntry).order_by(finance_model.FinanceEntry.date.desc()).all()

# ----------------------
# Update a transaction
# ----------------------
@router.put("/{transaction_id}", response_model=finance_schema.FinanceEntryResponse)
def update_transaction(
    transaction_id: int,
    entry: finance_schema.FinanceEntryUpdate,
    db: Session = Depends(get_db)
):
    transaction = db.query(finance_model.FinanceEntry).filter(
        finance_model.FinanceEntry.id == transaction_id
    ).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    for key, value in entry.dict(exclude_unset=True).items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)
    return transaction

# ----------------------
# Delete a transaction
# ----------------------
@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(finance_model.FinanceEntry).filter(
        finance_model.FinanceEntry.id == transaction_id
    ).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}
