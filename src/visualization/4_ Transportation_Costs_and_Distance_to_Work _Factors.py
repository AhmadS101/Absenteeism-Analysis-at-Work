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

""" 
Now let's analyze how Transportation Cost and Distance to Work impact Absenteeism Time.
These factors may influence absence, and since these variables are continuous, we'll examine the correlation between them.
"""

# plot transportation costs and distance to work against hours
plt.figure(figsize=(10, 5))
sns.jointplot(
    data=preprocessed_data,
    x="Distance from Residence to Work",
    y="Absenteeism time in hours",
    kind="reg",
)
plt.savefig("../../reports/figures/16_distance_vs_hours.png", format="png")

sns.jointplot(
    data=preprocessed_data,
    x="Transportation expense",
    y="Absenteeism time in hours",
    kind="reg",
)
plt.savefig("../../reports/figures/17_costs_vs_hours.png", format="png")
""" 
It seems there are some positive and negative correlations, but the distribution of absent hours
doesn't follow a normal distribution. This makes comparing the variables difficult to interpret.
One solution is to transform the data into something closer to a normal distribution using 
the Box-Cox or Yeo-Johnson transformations.
"""
# Check if the variables contain zeros. If not, use the Box-Cox transformation. If they do, use the Yeo-Johnson transformation.
print(preprocessed_data["Absenteeism time in hours"].isin([0]).sum())
# run Yeo-Johnson transformation and recreate previous plots
from scipy.stats import yeojohnson

hours = yeojohnson(preprocessed_data["Absenteeism time in hours"].apply((float)))
distances = preprocessed_data["Distance from Residence to Work"]
expenses = preprocessed_data["Transportation expense"]

plt.figure(figsize=(20, 10))
ax = sns.jointplot(x=distances, y=hours[0], kind="reg")
ax.set_axis_labels(
    "Distance from Residence to Work", "Transformed absenteeism time in hours"
)
plt.savefig("../../reports/figures/18_distance_vs_hours_transformed.png", format="png")

ax = sns.jointplot(x=expenses, y=hours[0], kind="reg")
ax.set_axis_labels("Transportation expense", "Transformed absenteeism time in hours")
plt.savefig("../../reports/figures/19_costs_vs_hours_transformed.png", format="png")

""" 
The regression line for the Distance from Residence to Work column is nearly flat, 
indicating zero correlation. In contrast, the Transportation Expense column shows 
a slight upward slope, suggesting a small positive correlation."""

# investigate correlation between the columns, Null Hypothese is no correlation
from scipy.stats import pearsonr

distance_corr = pearsonr(hours[0], distances)
expenses_corr = pearsonr(hours[0], expenses)

print(
    f"Distances correlation: corr={distance_corr[0]:.3f} | pvalue={distance_corr[1]:.3f}"
)
print(
    f"Expenses comparison:  corr={expenses_corr[0]:.3f}, | pvalue={expenses_corr[1]:.3f}"
)
"""
These results confirm our observation, stating that there is a slight positive 
correlation between Transportation expense and Absenteeism time in hours
    """
