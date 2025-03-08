from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
import datetime
import pandas as pd
from src.google_sheets import append_expense, get_expense_data
from openai import OpenAI
from config.settings import OPENAI_API_KEY
from src.ai_parser import parse_expense

# Initialize AI model
client = OpenAI(api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=OPENAI_API_KEY)

@tool
def log_expense(text: str):
    """Logs an expense into Google Sheets."""
    amount, category, date = parse_expense(text)
    append_expense(date, amount, category, text)
    return f"✅ Expense logged: {amount} for {category} on {date}"

@tool
def get_summary(query: str):
    """Fetches summary of expenses based on user query."""
    df = get_expense_data()

    if df.empty:
        return "No expenses found."

    if "today" in query:
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        df = df[df["Date"] == today]

    total_spent = df["Amount"].sum()
    response = f"Total: ₹{total_spent}\n\n"
    for _, row in df.iterrows():
        response += f"{row['Date']} - ₹{row['Amount']} ({row['Category']})\n"

    return response

tools = [log_expense, get_summary]
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
