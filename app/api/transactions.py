from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from fastapi import APIRouter, Depends, Query
from datetime import datetime


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#create a new transaction
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


@router.get("/transactions/")
def get_all_transactions(
    category: str | None = Query(default=None),
    transaction_type: str | None = Query(default=None),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)

    if category:
        query = query.filter(Transaction.category == category)

    if transaction_type:
        query = query.filter(
            Transaction.transaction_type == transaction_type
        )

    if start_date:
        query = query.filter(
            Transaction.created_at >= start_date
        )

    if end_date:
        query = query.filter(
            Transaction.created_at <= end_date
        )

    return query.all()


@router.get("/transactions/summary")
def get_transaction_summary(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()

    total_income = 0
    total_expense = 0
    category_wise_expense = {}

    for transaction in transactions:

        if transaction.transaction_type == "income":
            total_income += transaction.amount

        elif transaction.transaction_type == "expense":
            total_expense += transaction.amount

            category = transaction.category

            if category not in category_wise_expense:
                category_wise_expense[category] = 0

            category_wise_expense[category] += transaction.amount

    balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "category_wise_expense": category_wise_expense
    }



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



@router.put("/transactions/{transaction_id}")
def update_transaction(
    transaction_id: int,
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    existing_transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not existing_transaction:
        return {"message": "Transaction not found"}

    existing_transaction.amount = transaction.amount
    existing_transaction.category = transaction.category
    existing_transaction.description = transaction.description
    existing_transaction.transaction_type = transaction.transaction_type

    db.commit()
    db.refresh(existing_transaction)

    return existing_transaction