from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/transactions/")
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    new_transaction = Transaction(
        amount=transaction.amount,
        category=transaction.category,
        description=transaction.description,
        transaction_type=transaction.transaction_type
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@router.get("/transactions/{transaction_id}")
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        return {"message": "Transaction not found"}

    return transaction


@router.get("/transactions/summary")
def get_transaction_summary(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()

    summary = {}

    for transaction in transactions:
        category = transaction.category

        if category not in summary:
            summary[category] = 0

        summary[category] += transaction.amount

    return summary