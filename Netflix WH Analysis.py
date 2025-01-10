# pandas and matplotlib libraries will be used in this
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import ttest_ind
# For machine learning (clustering + KNN)
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import numpy as np

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

# LINE PLOT - Key Visualization for Hypothesis (Daily)
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

# HISTOGRAM - Distribution of Daily Watch Hours (All Data)
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

# Filtering Data from September 2022 for Separate Analysis
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

exam_periods = [ #Took from Academic Calendar
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

# Three-Monthly Aggregation 
quarterly_df = daily_watch_time[["Date_dt", "Duration"]].copy()
quarterly_df.set_index("Date_dt", inplace=True)

quarterly_agg = quarterly_df.resample("3ME").sum().reset_index()

quarterly_agg["Quarter_Label"] = quarterly_agg["Date_dt"].dt.strftime("%b %Y")

plt.figure(figsize=(10, 5))
plt.plot(
    quarterly_agg["Date_dt"],
    quarterly_agg["Duration"],
    marker='o',
    color='red',
    label='3-Month Watch Hours'
)
plt.title("Netflix Watch Hours - 3-Month Aggregation")
plt.xlabel("Quarter End")
plt.ylabel("Total Watch Hours (3-month sum)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Box Plot by Year
yearly_data = daily_watch_time.copy()
yearly_data["year"] = yearly_data["Date_dt"].dt.year

# We'll gather daily durations for each year and feed them to boxplot.
unique_years = sorted(yearly_data["year"].dropna().unique())
data_by_year = [yearly_data[yearly_data["year"] == y]["Duration"].dropna() for y in unique_years]

plt.figure(figsize=(8, 5))
plt.boxplot(data_by_year, vert=True, patch_artist=True, labels=[str(int(y)) for y in unique_years])
plt.title("Yearly Box Plot of Daily Watch Hours")
plt.xlabel("Year")
plt.ylabel("Daily Watch Hours")
plt.tight_layout()
plt.show()

# Machine Learning: kMM Implementation
class kMM:
    def __init__(self, n_clusters=3, random_state=None):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self._kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state)
        self.labels_ = None
        self.cluster_centers_ = None

    def fit(self, X):
        self._kmeans.fit(X)
        self.labels_ = self._kmeans.labels_
        self.cluster_centers_ = self._kmeans.cluster_centers_

    def predict(self, X):
        return self._kmeans.predict(X)

clustering_df = daily_watch_time.copy()
clustering_df["day_of_week"] = clustering_df["Date_dt"].dt.dayofweek.fillna(0)
clustering_df["Duration"] = clustering_df["Duration"].fillna(0)

X_kmm = clustering_df[["Duration", "day_of_week"]]

kmm_model = kMM(n_clusters=3, random_state=42)
kmm_model.fit(X_kmm)
clustering_df["kmm_label"] = kmm_model.labels_

print("\n=== k-MM Clustering Results ===")
print("Cluster centers (Duration, day_of_week):")
print(kmm_model.cluster_centers_)

cluster_counts = clustering_df["kmm_label"].value_counts()
print("\nNumber of days in each kMM cluster:")
print(cluster_counts)

plt.figure(figsize=(8, 5))
scatter_kmm = plt.scatter(
    clustering_df["day_of_week"],
    clustering_df["Duration"],
    c=clustering_df["kmm_label"],
    cmap="plasma"
)
plt.colorbar(scatter_kmm, label="kMM Cluster Label")
plt.title("kMM Clustering: Duration vs. Day of Week")
plt.xlabel("Day of Week (Mon=0, Sun=6)")
plt.ylabel("Daily Watch Hours")
plt.tight_layout()
plt.show()

# KNN Regression: Plot Predicted vs. Actual
knn_df = daily_watch_time.copy()
knn_df["day_of_week"] = knn_df["Date_dt"].dt.dayofweek
knn_df = knn_df.dropna(subset=["day_of_week", "Duration"])  # drop rows with missing values

# Features (X) and target (y)
X = knn_df[["day_of_week"]]
y = knn_df["Duration"]

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build and train the KNN model
knn_model = KNeighborsRegressor(n_neighbors=3)
knn_model.fit(X_train, y_train)

# Predict on the test set
y_pred = knn_model.predict(X_test)

# Merge test data with predictions for plotting
test_results = pd.DataFrame({
    "day_of_week": X_test["day_of_week"],
    "actual": y_test,
    "predicted": y_pred
})

# Sort by day_of_week for a cleaner line plot
test_results.sort_values(by="day_of_week", inplace=True)

# Plot actual vs. predicted as separate lines
plt.figure(figsize=(8, 5))
plt.plot(test_results["day_of_week"], test_results["actual"], label="Actual", marker='o')
plt.plot(test_results["day_of_week"], test_results["predicted"], label="Predicted", marker='x')
plt.title("KNN Regression: Actual vs. Predicted Daily Watch Hours")
plt.xlabel("Day of Week (Mon=0, Sun=6)")
plt.ylabel("Watch Hours")
plt.legend()
plt.tight_layout()
plt.show()