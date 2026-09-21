import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.3,
    google_api_key=os.getenv("GEMINI_API_KEY")
)


def generate_financial_insight(summary):

    total_income = summary["total_income"]
    total_expense = summary["total_expense"]
    balance = summary["balance"]
    category_wise_expense = summary["category_wise_expense"]

    # Case 1: Only expenses
    if total_income == 0 and total_expense > 0:

        prompt = f"""
You are a personal finance assistant.

The user has recorded expenses in the application,
but no income has been recorded.

Financial data:

Total expense: ₹{total_expense}

Category-wise expenses:
{category_wise_expense}

Give a short and practical financial insight.

Mention:
1. The total amount spent.
2. The highest spending category.
3. Clearly say that no income has been recorded in the application.
4. Give one practical suggestion.

Important:
Do not say that the user has no income in real life.
Only say that no income has been recorded in the application.

Do not invent any financial data.
"""

    # Case 2: Only income
    elif total_income > 0 and total_expense == 0:

        prompt = f"""
You are a personal finance assistant.

The user has recorded income in the application,
but no expenses have been recorded.

Financial data:

Total income: ₹{total_income}

Give a short and practical financial insight.

Mention:
1. The recorded income.
2. Clearly say that no expenses have been recorded.
3. Give one practical suggestion for tracking future spending.

Do not invent any financial data.
"""

    # Case 3: Both income and expenses
    else:

        prompt = f"""
You are a personal finance assistant.

Analyze the following financial data:

Total income: ₹{total_income}
Total expense: ₹{total_expense}
Balance: ₹{balance}

Category-wise expenses:
{category_wise_expense}

Give a short and practical financial insight.

Mention:
1. The user's spending situation.
2. The highest spending category.
3. The current balance.
4. One practical suggestion.

Do not invent any financial data.
"""

    response = llm.invoke(prompt)

    # Gemini may return structured content
    if isinstance(response.content, list):

        text_parts = []

        for item in response.content:

            if isinstance(item, dict):
                text = item.get("text")

                if text:
                    text_parts.append(text)

        return "".join(text_parts).strip()

    return str(response.content).strip()