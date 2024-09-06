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

# printing the actual count for social drinker and smoker

print(preprocessed_data["Social drinker"].value_counts(normalize=True))
print(preprocessed_data["Social smoker"].value_counts(normalize=True))

# Analysis of the distribution of social drinkers and smokers on each absence reason

plt.figure()
sns.countplot(
    data=preprocessed_data,
    x="Reason for absence",
    hue="Social drinker",
    hue_order=["Yes", "No"],
    palette="Set1",
)
plt.title("Absence reasons drinkers")
plt.ylabel("Number of entries per reason of absence")
plt.savefig("../../reports/figures/02_Absence_reasons_drinkers.png", format="png")

plt.figure()
sns.countplot(
    data=preprocessed_data,
    x="Reason for absence",
    hue="Social smoker",
    hue_order=["Yes", "No"],
    palette="Set1",
)
plt.title("Absence reasons smokers")
plt.ylabel("Number of entries per reason of absence")
plt.savefig("../../reports/figures/03_Absence_reasons_smokers.png", format="png")


""" 
Looking at the data, social drinking seems to influence reasons for absence, especially for dental consultations. 
However, since only 7% of the entries are from social smokers, it's hard to determine if smoking has any impact onabsences. 
To understand the effect of social drinking and smoking on absences better, we need to use conditional probability
"""

# ------------------------------------------------------------------------------------------

# Identifying Reasons of Absence with Higher Probability Among Drinkers and Smokers
#  computing conditional probabilities of the different reasons for absence

drinker_prob = preprocessed_data["Social drinker"].value_counts(normalize=True)["Yes"]
smoker_prob = preprocessed_data["Social smoker"].value_counts(normalize=True)["Yes"]
print(
    f"p(social drinker) = {drinker_prob :.3f} | p(social smoker) = {smoker_prob :.3f}"
)
# create mask for social drinkers/smokers
drinker_mask = preprocessed_data["Social drinker"] == "Yes"
smoker_mask = preprocessed_data["Social smoker"] == "Yes"
# Compute the total number of entries and the number of absence reasons
total_entries = preprocessed_data.shape[0]
absence_drinker_prob = (
    preprocessed_data["Reason for absence"][drinker_mask].value_counts() / total_entries
)
absence_smoker_prob = (
    preprocessed_data["Reason for absence"][smoker_mask].value_counts() / total_entries
)
# Compute the conditional probabilities by dividing the computed probabilities for each reason of absence
cond_prob = pd.DataFrame(index=range(0, 29))
cond_prob["P(Absence | social drinker)"] = absence_drinker_prob / drinker_prob
cond_prob["P(Absence | social smoker)"] = absence_smoker_prob / smoker_prob

plt.figure()
ax = cond_prob.plot.bar()
ax.set_ylabel("Conditional probability")
ax.set_title("conditional probabilities for absence")
plt.savefig("../../reports/figures/04_conditional_probabilities.png", format="png")

# ------------------------------------------------------------------------------------------

# Identifying the Probability of Being a Drinker/Smoker, Conditioned to Absence Reason
absence_prob = preprocessed_data["Reason for absence"].value_counts(normalize=True)
# compute conditional probabilities for drinker/smoker
cond_prob_drinker_smoker = pd.DataFrame(index=range(0, 29))
cond_prob_drinker_smoker["P(social drinker | Absence)"] = (
    cond_prob["P(Absence | social drinker)"] * drinker_prob / absence_prob
)
cond_prob_drinker_smoker["P(social smoker | Absence)"] = (
    cond_prob["P(Absence | social smoker)"] * smoker_prob / absence_prob
)

plt.figure()
ax = cond_prob_drinker_smoker.plot.bar()
ax.set_ylabel("Conditional probability")
ax.set_title("conditional probabilities drinker smoker")
plt.savefig(
    "../../reports/figures/05_conditional_probabilities_drinker_smoker.png",
    format="png",
)

# ------------------------------------------------------------------------------------------

# create violin plots of the absenteeism time in hours to calculate the distribution
ax = sns.violinplot(
    x="Social drinker",
    y="Absenteeism time in hours",
    data=preprocessed_data,
    order=["Yes", "No"],
)
ax.set_title("Violin plots of the absenteeism time in hours for social drinkers")
plt.savefig("../../reports/figures/06_drinkers_hour_distribution.png", format="png")

ax = sns.violinplot(
    x="Social smoker",
    y="Absenteeism time in hours",
    data=preprocessed_data,
    order=["Yes", "No"],
)
ax.set_title("Violin plots of the absenteeism time in hours for social smokers")
plt.savefig("../../reports/figures/07_smokers_hour_distribution.png", format="png")


""" 
The observation from figures, there's a despite some differences in the outliers between smokers and non-smokers, 
there is no substantial difference in the distribution of absenteeism hours in drinkers and smokers. 

To assess this statement in a rigorous statistical way, perform hypothesis testing on the absenteeism hours 
(with a null hypothesis stating that the average absenteeism time in hours is the same for drinkers and non-drinkers)
"""

# ------------------------------------------------------------------------------------------

from scipy.stats import ttest_ind

hours_col = "Absenteeism time in hours"
# test mean absenteeism time for drinkers
drinker_mask = preprocessed_data["Social drinker"] == "Yes"
hours_drinkers = preprocessed_data.loc[drinker_mask, hours_col]
hours_non_drinkers = preprocessed_data.loc[~drinker_mask, hours_col]

drinkers_test = ttest_ind(hours_drinkers, hours_non_drinkers)
print(f"Statistic value: {drinkers_test[0]}, p-value: {drinkers_test[1]}")

# test mean absenteeism time for smokers
smoker_mask = preprocessed_data["Social smoker"] == "Yes"
hours_smokers = preprocessed_data.loc[smoker_mask, hours_col]
hours_non_smokers = preprocessed_data.loc[~smoker_mask, hours_col]

smokers_test = ttest_ind(hours_smokers, hours_non_smokers)
print(f"Statistic value: {smokers_test[0]}, p-value: {smokers_test[1]}")

""" 
The p-value of both tests is above the critical value of 0.05, which means that you cannot reject the null hypothesis.
In other words, you cannot say that there is a statistically significant difference in the absenteeism hours 
between drinkers (and smokers) and non-drinkers (and non-smokers).

The average hours may still be equal, but their distributions may be different.  a Kolmogorov-Smirnov test to assess 
the difference in the distributions of two samples.
"""

# ------------------------------------------------------------------------------------------

# perform Kolmogorov-Smirnov test for comparing the distributions
from scipy.stats import ks_2samp

ks_drinkers = ks_2samp(hours_drinkers, hours_non_drinkers)
print(
    f"Drinkers comparison: statistics={ks_drinkers[0]:.3f}, pvalue={ks_drinkers[1]:.3f}"
)
ks_smokers = ks_2samp(hours_smokers, hours_non_smokers)
print(
    f"Smokers comparison:  statistics={ks_smokers[0]:.3f}, pvalue={ks_smokers[1]:.3f}"
)


""" 
The p-value for the drinkers dataset is lower than the critical 0.05, which is strong evidence against 
the null hypothesis of the two distributions being equal. On the other hand, as the p-value for the smokers 
dataset is higher than 0.05, you cannot reject the null hypothesis.
"""
