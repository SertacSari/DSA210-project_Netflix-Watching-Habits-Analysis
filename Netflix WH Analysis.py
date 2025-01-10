# pandas and matplotlib libraries will be used in this
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import ttest_ind

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

# Convert 'Date' from date object to string (day-month-year)
daily_watch_time["Date_str"] = daily_watch_time["Date"].apply(
    lambda d: d.strftime("%d-%m-%Y") if pd.notnull(d) else ""
)

# Also keep a proper datetime column for sorting and filtering
daily_watch_time["Date_dt"] = pd.to_datetime(daily_watch_time["Date_str"], format="%d-%m-%Y", errors="coerce")

# Sort by Date_dt
daily_watch_time.sort_values(by="Date_dt", inplace=True)

# Print for inspection
print("\n=== (ALL) Total Daily Watch Hours ===")
print(daily_watch_time[["Date_str", "Duration"]])

# LINE PLOT - Key Visualization for Hypothesis
plt.figure(figsize=(10, 5))
plt.plot(
    daily_watch_time["Date_dt"],
    daily_watch_time["Duration"],
    marker='o',
    linestyle='-',
    color='blue',
    label='Daily Watch Hours'
)
plt.title("Daily Netflix Watch Hours - Line Plot (All Data)")
plt.xlabel("Date (day-month-year)")
plt.ylabel("Watch Hours")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# BAR CHART - Another View of the Same Data
plt.figure(figsize=(10, 5))
plt.bar(
    daily_watch_time["Date_dt"].astype(str),
    daily_watch_time["Duration"],
    color='green',
    label='Daily Watch Hours'
)
plt.title("Daily Netflix Watch Hours - Bar Chart (All Data)")
plt.xlabel("Date (day-month-year)")
plt.ylabel("Watch Hours")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# HISTOGRAM - Distribution of Daily Watch Hours
plt.figure(figsize=(8, 5))
plt.hist(
    daily_watch_time["Duration"],
    bins=10,
    color='orange',
    edgecolor='black'
)
plt.title("Distribution of Daily Netflix Watch Hours - All Data")
plt.xlabel("Watch Hours per Day")
plt.ylabel("Frequency (Number of Days)")
plt.tight_layout()
plt.show()

# Only keep data >= 1st September 2022
start_sep_2022 = datetime.strptime("01-09-2022", "%d-%m-%Y")
filtered_df = daily_watch_time[daily_watch_time["Date_dt"] >= start_sep_2022].copy()

print("\n=== (SINCE SEP 2022) Total Daily Watch Hours ===")
print(filtered_df[["Date_str", "Duration"]])

# LINE PLOT for Filtered Data
plt.figure(figsize=(10, 5))
plt.plot(
    filtered_df["Date_dt"],
    filtered_df["Duration"],
    marker='o',
    linestyle='-',
    color='blue',
    label='Daily Watch Hours (Since Sep 2022)'
)
plt.title("Daily Netflix Watch Hours - Line Plot (Since Sep 2022)")
plt.xlabel("Date (day-month-year)")
plt.ylabel("Watch Hours")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# BAR CHART for Filtered Data
plt.figure(figsize=(10, 5))
plt.bar(
    filtered_df["Date_dt"].astype(str),
    filtered_df["Duration"],
    color='green',
    label='Daily Watch Hours (Since Sep 2022)'
)
plt.title("Daily Netflix Watch Hours - Bar Chart (Since Sep 2022)")
plt.xlabel("Date (day-month-year)")
plt.ylabel("Watch Hours")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()



# Final exam dates:
# 1) 02-18 Jan 2023
# 2) 01-11 Jun 2023
# 3) 06-19 Jan 2024
# 4) 30 May - 09 Jun 2024
# 5) 24-27 Aug 2024

exam_periods = [
    ("02-01-2023", "18-01-2023"),
    ("01-06-2023", "11-06-2023"),
    ("06-01-2024", "19-01-2024"),
    ("30-05-2024", "09-06-2024"),
    ("24-08-2024", "27-08-2024"),
]

# Convert them to datetime objects
exam_periods_dt = []
for start_str, end_str in exam_periods:
    start_dt = datetime.strptime(start_str, "%d-%m-%Y")
    end_dt   = datetime.strptime(end_str,   "%d-%m-%Y")
    exam_periods_dt.append((start_dt, end_dt))

# Create a function to check if a given date is in any exam period
def is_in_exam_period(date_dt, periods):
    for (s, e) in periods:
        if s <= date_dt <= e:
            return True
    return False

# Apply this function to create a boolean column
daily_watch_time["IsExamPeriod"] = daily_watch_time["Date_dt"].apply(
    lambda d: is_in_exam_period(d, exam_periods_dt)
)

# Separate data into Exam vs. Non-exam
exam_df = daily_watch_time[daily_watch_time["IsExamPeriod"] == True]
non_exam_df = daily_watch_time[daily_watch_time["IsExamPeriod"] == False]

# Compute mean watch hours
exam_mean = exam_df["Duration"].mean()
non_exam_mean = non_exam_df["Duration"].mean()

print("\n=== Exam Period Mean: {:.2f} hours/day ===".format(exam_mean))
print("=== Non-Exam Period Mean: {:.2f} hours/day ===".format(non_exam_mean))

# T-test to see if the difference is statistically significant
t_stat, p_val = ttest_ind(
    exam_df["Duration"].dropna(),
    non_exam_df["Duration"].dropna(),
    equal_var=False  # Welch's t-test
)

print("\n=== T-Test Results (All Exam Periods Combined) ===")
print(f"T-statistic: {t_stat:.3f}")
print(f"P-value: {p_val:.3f}")
print("Note: If p-value < 0.05, there's a significant difference.\n")
