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
preprocessed_data.head().T

# Identifying Reasons for Absence
"""
define function, which checks if the provided integer value
is contained in the ICD or not, then append a disease column as binary to df
"""


def in_icd(val):
    return "Yes" if val >= 1 and val <= 21 else "No"


preprocessed_data["Disease"] = preprocessed_data["Reason for absence"].apply(in_icd)

# using bar plot to compare the absences due to disease resons or not
plt.figure()
sns.countplot(data=preprocessed_data, x="Disease")
plt.savefig("../../reports/figures/00_disease_resons_plot.png", format="png")

""" 
from the first observation, we see that the ICD disease isn't the main reason for the absence.
So for more details of absence reasons, we need to ask some questions 
"What is the most common reason for absence?" 
"Does being a drinker or smoker has some effect on the causes?"  
"Does the distance to work have some effect on the reasons? "
" Does Transportation expense have some effect on absence and so on?
"""

# Analysis for getting the number of entries for each reason for absence
plt.figure()
ax = sns.countplot(data=preprocessed_data, x="Reason for absence")
ax.set_ylabel("Number of entries per reason of absence")
plt.savefig("../../reports/figures/01_absence_reasons_distribution.png", format="png")

""" 
From this observation, it is clear that the main reasons for absence are not related to ICD,
most frequent reasons for absence are related to medical consultations (23), dental consultations (28), 
and physiotherapy (27).
On the other hand, there're reasons for absence encoded in the ICD encoding are related to diseases of 
the musculoskeletal system and connective tissue (13) and injury, poisoning, and certain other consequences 
of external causes (19)
"""
