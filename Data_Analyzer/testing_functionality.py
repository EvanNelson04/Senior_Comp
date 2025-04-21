import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("../creds.json", scope)
client = gspread.authorize(creds)

# Try opening your Google Sheet
spreadsheet = client.open("Workouts")  # replace this
print("✅ Connection successful! Sheet title:", spreadsheet.title)
