from langchain_core.tools import tool

from app.database.database import SessionLocal
from app.models.transaction import Transaction


@tool
def get_spending_summary():
    """Get total spending grouped by category from the database."""

    db = SessionLocal()

    try:
        transactions = db.query(Transaction).all()

        summary = {}

        for transaction in transactions:
            category = transaction.category

            if category not in summary:
                summary[category] = 0

            summary[category] += transaction.amount

        return summary

    finally:
        db.close()


@tool
def get_total_spending():
    """Get the total amount spent across all transactions."""

    db = SessionLocal()

    try:
        transactions = db.query(Transaction).all()

        total = 0

        for transaction in transactions:
            total += transaction.amount

        return total

    finally:
        db.close()


@tool
def get_transactions():
    """Get all transactions from the database."""

    db = SessionLocal()

    try:
        transactions = db.query(Transaction).all()

        result = []

        for transaction in transactions:
            result.append({
                "amount": transaction.amount,
                "category": transaction.category,
                "description": transaction.description,
                "transaction_type": transaction.transaction_type
            })

        return result

    finally:
        db.close()