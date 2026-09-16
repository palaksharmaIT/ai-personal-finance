from pydantic import BaseModel


class TransactionCreate(BaseModel):
    amount: float
    category: str
    description: str | None = None
    transaction_type: str