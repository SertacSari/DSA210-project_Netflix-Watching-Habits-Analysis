# pandas and matplotlib libraries will be used in this
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv(
    "ViewingActivity.csv",
    names=[
        "ProfileName",
        "StartTime",
        "Duration",
        "Attributes",
        "Title",
        "SupplementalVideoType",
        "DeviceType",
        "Bookmark",
        "LatestBookmark",
        "Country"
    ]
)

# Filter the Data for Profile Name: "Sertaç"
df = df[df["ProfileName"] == "Sertaç"]

# Convert 'StartTime' to a proper datetime format
df["StartTime"] = pd.to_datetime(
    df["StartTime"], 
    format="%Y-%m-%d %H:%M:%S",  
    errors="coerce"  # Turn invalid parsing into NaT
)

# Extract only the Date (yyyy-mm-dd) from 'StartTime'
df["Date"] = df["StartTime"].dt.date

# Convert 'Duration' (HH:MM:SS) to hours
df["Duration"] = pd.to_timedelta(df["Duration"], errors="coerce").dt.total_seconds() / 3600

# Group by Date and sum the daily watch hours
daily_watch_time = df.groupby("Date")["Duration"].sum().reset_index()

# Convert 'Date' to the desired day-month-year (dd-mm-yyyy) format
# Note: 'daily_watch_time["Date"]' is a 'datetime.date' object, so we apply strftime in a lambda.
daily_watch_time["Date"] = daily_watch_time["Date"].apply(
    lambda d: d.strftime("%d-%m-%Y") if pd.notnull(d) else ""
)

# Print the daily watch time (for inspection)
print("\n=== Total Daily Watch Hours (Sertaç) ===")
print(daily_watch_time) 