from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.transaction import Transaction
from app.services.ai_service import generate_financial_insight


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/ai/financial-insight")
def financial_insight(
    db: Session = Depends(get_db)
):
    # Fetch all transactions from database
    transactions = db.query(Transaction).all()

    # Case 1: No transactions
    if not transactions:
        return {
            "message": "No transactions found. Please add some transactions to generate financial insights."
        }

    total_income = 0
    total_expense = 0
    category_wise_expense = {}

    # Extract data from transactions
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

    summary = {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "category_wise_expense": category_wise_expense
    }

    # Send financial data to Gemini
    insight = generate_financial_insight(summary)

    return {
        "summary": summary,
        "insight": insight
    }