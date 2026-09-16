import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from app.tools.finance_tools import (
    get_spending_summary,
    get_total_spending
)


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


agent = create_agent(
    model=llm,
    tools=[
        get_spending_summary,
        get_total_spending
    ]
)


user_question = "How much money have I spent in total?"


response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": user_question
        }
    ]
})


print("Agent response:")
print(response["messages"][-1].content)