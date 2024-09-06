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
In this section, we'll analyze the effect of body mass index (BMI) on employee absence. 
First, we'll create a function to categorize BMI and add these categories to the data frame. 
Then, we'll observe the distribution of each absence reason across the different BMI categories.
"""


#  define function for computing the BMI category, based on BMI value
def get_bmi_category(bmi):
    if bmi < 18.5:
        category = "underweight"
    elif bmi >= 18.5 and bmi < 25:
        category = "healthy weight"
    elif bmi >= 25 and bmi < 30:
        category = "overweight"
    else:
        category = "obese"
    return category


preprocessed_data["BMI category"] = preprocessed_data["Body mass index"].apply(
    get_bmi_category
)

plt.figure()
ax = sns.countplot(
    data=preprocessed_data,
    x="BMI category",
    order=["underweight", "healthy weight", "overweight", "obese"],
    palette="Set1",
)
ax.set_ylabel("Number of employees")
ax.set_title("BMI categories")
plt.savefig("../../reports/figures/08_bmi_categories.png", format="png")

"""
From the initial observation, there are no employees classified as underweight. 
This indicates that more than 60% of the employees are either overweight or obese
"""

# plot BMI categories vs Reason for absence
plt.figure(figsize=(20, 20))
ax = sns.countplot(
    data=preprocessed_data,
    y="Reason for absence",
    hue="BMI category",
    hue_order=["underweight", "healthy weight", "overweight", "obese"],
    palette="Set2",
)
ax.set_xlabel("Number of employees")
ax.set_title("Absence reasons, based on BMI category")
plt.savefig("../../reports/figures/09_reasons_bmi.png", format="png")

"""
no clear pattern emerges from the preceding plot. In other words, for each reason for absence, 
the number of employees across different body mass index categories is nearly equal.

we can use a bistribution of hours for the different BMI ategories
"""
sns.violinplot(
    data=preprocessed_data,
    x="BMI category",
    y="Absenteeism time in hours",
    palette="Set1",
)
plt.title("Absence time in hours, based on the BMI category")
plt.savefig("../../reports/figures/10_bmi_hour_distribution.png", format="png")

""" 
No evidence states that BMI and obesity levels influence the employees' absenteeism.
We can check our hypothies by using  Kruskal-Wallis test for comparing the distributions
"""

from scipy.stats import kruskal

health_weight = preprocessed_data["BMI category"] == "healthy weight"
overweight = preprocessed_data["BMI category"] == "overweight"
obese = preprocessed_data["BMI category"] == "obese"
Kruskal_BMI_cat = kruskal(health_weight, overweight, obese)
print(
    f"BMI Comparison:  Statistics={Kruskal_BMI_cat[0]:.3f}, P-Value={Kruskal_BMI_cat[1]:.3f}"
)

""" 
The p-value of Kruskal-Wallis test is above the critical value of 0.05, which means that you cannot reject the null hypothesis.
"""

# ------------------------------------------------------------------------------------------

#  Age and Education Factors

""" 
Age and education may also influence employees' absenteeism. we'll investigate the correlation 
between age and absence hours. We will create a regression plot,  We'll also include 
the Pearson's correlation coefficient and its p-value, where the null hypothesis is that 
the correlation coefficient between the two features is equal to zero.
"""

# compute Pearson's correlation coefficient and p-value
from scipy.stats import pearsonr

plt.figure(figsize=(10, 5))
pearson_test = pearsonr(
    preprocessed_data["Age"],
    preprocessed_data["Absenteeism time in hours"],
)
ax = sns.regplot(
    data=preprocessed_data,
    x="Age",
    y="Absenteeism time in hours",
    scatter_kws={"alpha": 0.5},
)
ax.set_title(f"Correlation= {pearson_test[0]:.03f} | P-Value= {pearson_test[1]:.03f}")
plt.savefig("../../reports/figures/11_correlation_age_hours.png", format="png")

""" 
The plot shows no significant pattern, as indicated by the very small correlation coefficient (0.066) and a p-value greater than 0.05, 
suggesting there is no relationship between Age and Absenteeism time in hours.
"""


# Investigating the Impact of Age on Reason for Absence, create violin plot between the Age and Disease columns
def in_icd(val):
    return "Yes" if val >= 1 and val <= 21 else "No"


preprocessed_data["Disease"] = preprocessed_data["Reason for absence"].apply(in_icd)

sns.violinplot(data=preprocessed_data, x="Disease", y="Age", palette="Set1")
plt.savefig(
    "../../reports/figures/12_Violin_plot_for_disease_versus_age.png", format="png"
)

""" 
can see some differences between the two distributions of age.
"""

#  get Age entries for employees with Disease == Yes and Disease == No
disease_mask = preprocessed_data["Disease"] == "Yes"
disease_ages = preprocessed_data["Age"][disease_mask]
no_disease_ages = preprocessed_data["Age"][~disease_mask]

from scipy.stats import ttest_ind, ks_2samp

# perform hypothesis test for equality of means
test_result = ttest_ind(disease_ages, no_disease_ages)
print(
    f"Test for equality of means: statistic={test_result[0]:0.3f}, pvalue={test_result[1]:0.3f}"
)
# test equality of distributions via Kolmogorov-Smirnov test
ks_result = ks_2samp(disease_ages, no_disease_ages)
print(
    f"KS test for equality of distributions: statistic={ks_result[0]:0.3f}, pvalue={ks_result[1]:0.3f}"
)

""" 
The results of the two tests indicate no statistically significant difference between the distributions. 
Therefore, age does not influence the length or type of absence.
"""

# investigate the relationship between age and reason for absence
sns.violinplot(data=preprocessed_data, x="Reason for absence", y="Age", palette="Set1")
plt.savefig("Violin plot for age and reason for absence")
plt.savefig(
    "../../reports/figures/13_Violin plot_for_age_and_reason_for_absence.png",
    format="png",
)

""" 
a weak and inconsistent relationship between age and reasons for absence, with varied age distributions
and no dominant age group for any specific reason.
"""

# ------------------------------------------------------------------------------------------

# Investigating the Impact of Education on Reason for Absence
education_types = ["high_school", "graduate", "postgraduate", "master_phd"]
counts = preprocessed_data["Education"].value_counts()
percentages = preprocessed_data["Education"].value_counts(normalize=True)

for educ_type in education_types:
    print(
        f"Education type: {educ_type:12s} | Counts: {counts[educ_type]:6.0f} | Percentage: {100*percentages[educ_type]:4.1f}"
    )
"""
The data shows a strong bias, as the majority of employees (82.6%) have a high school degree.
"""

# distribution of absence hours, based on education level
sns.violinplot(
    data=preprocessed_data,
    x="Education",
    y="Absenteeism time in hours",
    palette="Set2",
    order=["high_school", "graduate", "postgraduate", "master_phd"],
)
plt.title(" number of hours of absence for each level of education")
plt.savefig(
    "../../reports/figures/14_ number_of_hours_of_absence_for_each_level_of_education.png",
    format="png",
)
"""
The plot suggests a significant variation in absenteeism hours among high school graduates, 
with some taking a substantial number of hours off. In contrast, employees with 
higher education levels tend to have fewer and more consistent absenteeism hours.
"""

# compute mean and standard deviation of absence hours
for educ_type in education_types:
    mask = preprocessed_data["Education"] == educ_type
    hours = preprocessed_data["Absenteeism time in hours"][mask]
    mean = hours.mean()
    stddev = hours.std()
    print(
        f"Education type: {educ_type:12s} | Mean : {mean:.03f} | Stddev: {stddev:.03f}"
    )
""" 
Both the mean and standard deviation of absence hours decrease with higher education levels, 
indicating that more educated employees tend to have shorter absences. However, 
education level is likely an indicator rather than a direct cause of this trend.
"""

# plot reason for absence, based on education level
plt.figure(figsize=(10, 15))
sns.countplot(
    data=preprocessed_data,
    y="Reason for absence",
    hue="Education",
    hue_order=["high_school", "graduate", "postgraduate", "master_phd"],
    palette="Set1",
)
plt.title(" Reasons for absence for each level of education")
plt.savefig(
    "../../reports/figures/15_ Reasons_for_absence_for_each_level_of_education.png",
    format="png",
)

""" 
From the preceding plot, you can observe that most of the absences relate to employees with a high_school level
of education. This is, of course, due to the fact that most of the employees only have a high school degree.
So we will use the codtional probability to observe that absent for more than one working week (40 hours) is greater 
for employees with a high school degree compared to graduates.
"""

# define threshold for extreme hours of absenteeism and get total number of entries
threshold = 40
total_entries = len(preprocessed_data)
# find entries with Education == high_school
high_school_mask = preprocessed_data["Education"] == "high_school"
# find entries with absenteeism time in hours more than threshold
extreme_mask = preprocessed_data["Absenteeism time in hours"] > threshold
# compute probability of having high school degree
prob_high_school = len(preprocessed_data[high_school_mask]) / total_entries
# compute probability of having more than high school degree
prob_graduate = len(preprocessed_data[~high_school_mask]) / total_entries
#  compute probability of having high school and being absent for more than "threshold" hours
prob_extreme_high_school = (
    len(preprocessed_data[high_school_mask & extreme_mask]) / total_entries
)
prob_extreme_graduate = (
    len(preprocessed_data[~high_school_mask & extreme_mask]) / total_entries
)
# compute and print conditional probabilities
cond_prob_extreme_high_school = prob_extreme_high_school / prob_high_school
cond_prob_extreme_graduate = prob_extreme_graduate / prob_graduate

print(
    f"P(extreme absence | degree = high_school) = {100*cond_prob_extreme_high_school:.3f}"
)
print(
    f"P(extreme absence | degree != high_school) = {100*cond_prob_extreme_graduate:.3f}"
)
"""
Based on the calculations, the probability of an employee with a high school degree having an absence of more than 40 hours is 2.29%.
This is nearly three times higher than the probability for employees with a university degree, which is 0.78%.
"""
