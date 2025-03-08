from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def parse_expense(text):
    """Uses OpenAI to extract amount, category, and date from text"""
    prompt = f"""
    Extract the amount, category, and date from this expense statement:
    "{text}"
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
