import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("../creds.json", scope)
client = gspread.authorize(creds)

# Open Google Sheet
spreadsheet = client.open("Workouts")
sheet = spreadsheet.sheet1

# Convert to DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Convert workout time to minutes
def duration_to_minutes(t):
    """Convert time on spreadsheet to minutes, rounded to 2 decimal places."""
    try:
        h, m, s = map(int, t.replace("h", "").replace("m", "").replace("s", "").split(":"))
        minutes = h * 60 + m + s / 60
        return round(minutes, 2)
    except:
        return 0

df["Duration_min"] = df["Total Time"].apply(duration_to_minutes)
df["Cal/min"] = round(df["Active Calories"] / df["Duration_min"], 2)
df["HR Zone"] = pd.cut(df["Avg. Heart Rate"], bins=[0, 100, 120, 140, 160, 200],
                       labels=["Very Light", "Light", "Moderate", "Hard", "Max"])

# Simple evaluation logic
def evaluate(row):
    tags = []
    if row["Duration_min"] >= 50:
        tags.append("Good volume")
    if row["Cal/min"] >= 5:
        tags.append("High caloric output")
    if row.get("Heart Rate Stress Score", 0) > 10:
        tags.append("High stress score")
    if row["HR Zone"] in ["Hard", "Max"]:
        tags.append("High HR zone")
    return ", ".join(tags) if tags else "Moderate workout"

df["Evaluation"] = df.apply(evaluate, axis=1)

# Output evaluations
print(df[["Date", "Type", "Duration_min", "Avg. Heart Rate","Max. Heart Rate", "Cal/min", "Evaluation"]])
