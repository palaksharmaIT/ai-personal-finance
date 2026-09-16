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


if __name__ == "__main__":
    result = get_spending_summary.invoke({})
    print(result)