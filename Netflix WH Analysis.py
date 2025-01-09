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
