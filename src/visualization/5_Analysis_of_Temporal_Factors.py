# --------------------------------------------------------------
# Importing Libraries
# --------------------------------------------------------------
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append("..")
import visualization.plot_settings

# --------------------------------------------------------------
# Loading Data
# --------------------------------------------------------------
preprocessed_data = pd.read_pickle("../../data/interim/00_preprocessed_data.plk")

"""" 
Factors like the day of the week and the month can also indicate absenteeism. For example, employees might 
choose to schedule their medical examinations on Fridays when the workload is lighter and the weekend is near.
"""
# count entries per day of the week and month
ax = sns.countplot(
    data=preprocessed_data,
    x="Day of the week",
    order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    palette="Set1",
)
ax.set_title("Number of absences per day of the week")
plt.savefig("../../reports/figures/20_dow_counts.png", format="png")

ax = sns.countplot(
    data=preprocessed_data,
    x="Month of absence",
    order=[
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
        "Unknown",
    ],
    palette="Set2",
)
ax.set_title("Number of absences per month")
plt.savefig("../../reports/figures/21_Number_of_absences per_month.png", format="png")
""" 
The plots don't show a big difference in absences between different days or months. There are fewer absences on Thursdays,
and March has the most absences, but the differences don't seem significant.
"""

# Analyzing Absence Hours by Day of the Week and Month of the Year.
sns.violinplot(
    data=preprocessed_data,
    x="Day of the week",
    y="Absenteeism time in hours",
    order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    palette="Set1",
)
plt.title("Average absent hours during the week")
plt.savefig("../../reports/figures/22_dow_hours.png", format="png")

sns.violinplot(
    data=preprocessed_data,
    x="Month of absence",
    y="Absenteeism time in hours",
    order=[
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
        "Unknown",
    ],
    palette="Set2",
)
plt.title("Average absent hours over the year")
plt.savefig("../../reports/figures/23_month_hours.png", format="png")

#  compute mean and standard deviation of absence hours per day of the week
dows = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
for dow in dows:
    mask = preprocessed_data["Day of the week"] == dow
    hours = preprocessed_data["Absenteeism time in hours"][mask]
    mean = hours.mean()
    stddev = hours.std()
    print(f"Day of the week: {dow:10s} | Mean : {mean:.03f} | Stddev: {stddev:.03f}")
