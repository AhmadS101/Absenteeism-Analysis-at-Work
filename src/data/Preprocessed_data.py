# --------------------------------------------------------------
# Importing libraries
# --------------------------------------------------------------

import pandas as pd

# --------------------------------------------------------------
# Importing Data
# --------------------------------------------------------------

abs_data = pd.read_csv(
    "../../data/raw/absenteeism+at+work/Absenteeism_at_work.csv", sep=";"
)

# --------------------------------------------------------------
# Processing data
# --------------------------------------------------------------
"""
Printing dimensionality of the data, columns, types, and missing values
"""
print(f"Data dimension: {abs_data.shape}")
for col in abs_data:
    print(
        f"column: {col:35} | type: {str(abs_data[col].dtype):7} | missing values: {abs_data[col].isna().sum() :3d}"
    )

# compute statistics on numerical features
abs_data.describe().T

# define encoding dictionaries
""" 
There is some categorical data encoded as numeric values. For this process, 
we'll create dictionaries to transform the data by mapping it.
"""
month_encoding = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
    0: "Unknown",
}

season_encoding = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}

dow_encoding = {2: "Monday", 3: "Tuesday", 4: "Wednesday", 5: "Thursday", 6: "Friday"}

education_encoding = {
    1: "high_school",
    2: "graduate",
    3: "postgraduate",
    4: "master_phd",
}
yes_no_encoding = {0: "No", 1: "Yes"}

# backtransform numerical variables to categorical
""" 
ِA new copy of the original data is created. This is a convenient way 
to create new pandas DataFrames, without taking the risk of modifying 
the original raw data (as it might serve us later).
"""
preprocessed_data = abs_data.copy()
preprocessed_data["Month of absence"] = preprocessed_data["Month of absence"].apply(
    lambda x: month_encoding[x]
)
preprocessed_data["Day of the week"] = preprocessed_data["Day of the week"].apply(
    lambda x: dow_encoding[x]
)
preprocessed_data["Seasons"] = preprocessed_data["Seasons"].apply(
    lambda x: season_encoding[x]
)
preprocessed_data["Education"] = preprocessed_data["Education"].apply(
    lambda x: education_encoding[x]
)
preprocessed_data["Disciplinary failure"] = preprocessed_data[
    "Disciplinary failure"
].apply(lambda X: yes_no_encoding[X])
preprocessed_data["Social drinker"] = preprocessed_data["Social drinker"].apply(
    lambda x: yes_no_encoding[x]
)
preprocessed_data["Social smoker"] = preprocessed_data["Social smoker"].apply(
    lambda x: yes_no_encoding[x]
)

preprocessed_data.head().T
# check the data types
for col in preprocessed_data:
    print(
        f"column: {col:35} | type: {str(preprocessed_data[col].dtype):7} | missing values: {preprocessed_data[col].isna().sum() :3d}"
    )

preprocessed_data.to_pickle("../../data/interim/00_preprocessed_data.plk")
