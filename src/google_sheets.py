import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from config.settings import GOOGLE_SHEETS_CREDENTIALS

# Authenticate Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS, scope)
client = gspread.authorize(creds)
sheet = client.open("Whatsapp Expense Tracker").sheet1

def append_expense(date, amount, category, text):
    """Appends an expense entry to Google Sheets."""
    sheet.append_row([date, amount, category, text])

def get_expense_data():
    """Retrieves all expenses as a DataFrame."""
    data = sheet.get_all_records()
    return pd.DataFrame(data)
