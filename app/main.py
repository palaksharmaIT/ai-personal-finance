from fastapi import FastAPI

from app.database.database import Base, engine
from app.models.transaction import Transaction
from app.api.transactions import router as transaction_router


Base.metadata.create_all(bind=engine)


app = FastAPI(title="AI Personal Finance Assistant")


app.include_router(transaction_router)


@app.get("/")
def home():
    return {"message": "Finance Assistant API is running"}