import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.tools.finance_tools import get_spending_summary


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


llm_with_tools = llm.bind_tools([
    get_spending_summary
])


response = llm_with_tools.invoke(
    "How much money have I spent in each category?"
)


print("Tool calls:")
print(response.tool_calls)


# Execute the tool
tool_result = get_spending_summary.invoke({})

print("\nTool result:")
print(tool_result)