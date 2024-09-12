# Absenteeism-Analysis-at-Work
Dive into the analysis of absenteeism at work and explore the various factors that influence time away from the job. Let's uncover the reasons driving absences and ask the right questions to understand their impact.
 Dive into the analysis of absenteeism at work and explore the various factors that influence time away from the job. 

 Let's uncover the reasons driving absences and ask the right questions to understand their impact.

## Overview 
This project delves into the analysis of workplace absenteeism by investigating several key factors that could influence time off. After preprocessing the data, the analysis examines the effects of being a social smoker or drinker, the influence of various diseases, and the impact of body mass, age, and education on absenteeism. Additionally, it explores how transportation costs and distance to work play a role in employee absences. By analyzing a real-world dataset, the project seeks to answer critical questions and test hypotheses through visualizations and statistical methods.

## Dataset 
**Title:** Absenteeism at work

**Source:** UC Irvine Machine Learning Repository

**Link:** https://archive.ics.uci.edu/dataset/445/absenteeism+at+work
---
**Description:** 
The dataset records employee absenteeism at a courier company in Brazil from July 2007 to July 2010. It reflects the shift towards trust-based work environments, where employees manage their own work hours. This flexibility, however, can lead to unregulated absenteeism, which may negatively affect productivity and employee evaluations. The data includes information on various factors such as reasons for absence, employee demographics, work conditions, and social habits, providing a comprehensive view to analyze the impact of these factors on absenteeism.

## Project Goals
- **Explore the data:** Checked the data, preprocessed it, and transformed it into a human-readable format.

- **Analyzing the impact of being a social smoker or drinker on reasons for absence:** The analysis indicates that social drinking may affect reasons for absence, particularly dental consultations, while the impact of social smoking is unclear due to a small sample size. Hypothesis testing shows no significant difference in absenteeism hours between drinkers and non-drinkers, or smokers and non-smokers. However, the Kolmogorov-Smirnov test suggests that the distribution of absenteeism hours differs between drinkers and non-drinkers, but not between smokers and non-smokers. This implies that while average absenteeism hours are similar, the patterns differ for drinkers.

- **Analysis of BodyMass Adge and Education on absence:**  This analysis examines the effects of BMI, age, and education on employee absenteeism. Findings indicate no significant relationship between BMI and absenteeism, as confirmed by statistical testing. Similarly, no correlation was found between age and absenteeism hours. The data is heavily biased toward employees with high school degrees, who also exhibit higher absenteeism rates. Specifically, employees with a high school degree are nearly three times more likely to have absences exceeding 40 hours compared to university graduates.

- **Analysis of Transportation Costs and Distance to Work Factors:** The analysis revealed no correlation between commute distance and absenteeism, but a slight positive link between transportation costs and absence hours. While higher travel expenses may contribute to increased absenteeism, the weak correlations suggest other factors likely have a more significant impact on employee attendance patterns.

- **Analysis of Temporal Factors:** The analysis of absenteeism patterns across days and months showed minor variations, with slightly fewer absences on Thursdays and more in March. However, these differences were not significant, suggesting that temporal factors have little impact on overall employee attendance patterns.

 ## Project Output
  - **Pyhon scripts for each step of project**:

    Script Sequence
    1. *Data Directory:*
        - Preprocessed_data.py
    3. *visualization Directory:*
       - 01_Initial_analysis.py
       - 02_ Analysis_of_Social_Drinkers_and_Smokers.py
       - 03_Analysis_of_BodyMass_Adge_and_Education_on_absence.py
       - 4_ Transportation_Costs_and_Distance_to_Work _Factors.py
       - 5_Analysis_of_Temporal_Factors
  - **Visualization Figures**
  - **Explanation of each section of code as comments**

---
This absenteeism analysis demonstrates the value of data analytics in revealing workplace insights. By examining various factors, it uncovers subtle trends in employee attendance, highlighting the importance of data-driven decision-making in human resource management and challenging preconceived notions about workforce behavior.
