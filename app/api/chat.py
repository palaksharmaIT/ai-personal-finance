from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agent import agent


router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat/")
def chat(request: ChatRequest):

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": request.question
            }
        ]
    })

    return {
        "response": response["messages"][-1].content
    }