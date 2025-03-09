from openai import OpenAI
import os
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_expense(text):
    """Uses OpenAI to extract amount, category, and date from text.
       - If no date is mentioned, it defaults to today.
       - If 'yesterday' is mentioned, it adjusts the date accordingly.
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    prompt = f"""
    Extract the amount, category, and date from this expense statement:
    "{text}"
    
    - If a date is mentioned (e.g., "March 7th"), extract it.
    - If "yesterday" is mentioned, set the date as {yesterday.strftime('%Y-%m-%d')}.
    - If no date is mentioned, set it as {today.strftime('%Y-%m-%d')}.
    
    Respond in this format: Amount: <amount>, Category: <category>, Date: <date>.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}]
    )

    parsed_text = response.choices[0].message.content

    # Extract values
    parts = parsed_text.split(", ")
    amount = parts[0].split(": ")[1]
    category = parts[1].split(": ")[1]
    date = parts[2].split(": ")[1]

    return amount, category, date
