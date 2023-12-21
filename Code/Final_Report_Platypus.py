#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:05:04 2023

@author: timbaettig
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.lines as mlines

directory = "/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data"
df = pd.read_csv('/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OUT_df/final_df_cleaned.csv', index_col=False)


"""
*******************************************************************************
Distribution Visualisation - Histograms
*******************************************************************************
"""

# Setting the aesthetics for the plots
sns.set(style="whitegrid")

# Descriptive statistics of the dataframe
descriptive_stats = df.describe()

# Plotting histograms for each variable to understand their distribution
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))
fig.suptitle('Histograms of Variables', fontsize=16)

sns.histplot(df['EPS'], bins=30, kde=True, ax=axes[0, 0])
axes[0, 0].set_title('Environmental Policy Stringency (EPS)')

sns.histplot(df['WIP'], bins=30, kde=True, ax=axes[0, 1])
axes[0, 1].set_title('Share of Women in Parliament (WIP)')

sns.histplot(df['Block'], bins=30, kde=True, ax=axes[1, 0])
axes[1, 0].set_title('Block')

sns.histplot(df['GDPpc'], bins=30, kde=True, ax=axes[1, 1])
axes[1, 1].set_title('GDP per Capita (GDPpc)')

sns.histplot(df['Education'].dropna(), bins=30, kde=True, ax=axes[2, 0])
axes[2, 0].set_title('Education (Tertiary)')

# Adjusting layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

#Saving Polot
path = "/OUT_plots/Alternative/Disribution_Key_Variables.pdf"
plt.savefig(directory + path)

# Displaying descriptive statistics
descriptive_stats


"""
*******************************************************************************
UNIVARIATE ANALYSIS
*******************************************************************************
"""

# Function to create a summary table and plot for each variable
def analyze_variable(data, variable, ax):
    # Summary statistics
    summary = data[variable].describe()
    # Plotting the distribution
    sns.histplot(data[variable], kde=True, ax=ax)
    ax.set_title(f'Distribution of {variable}')
    return summary

# Creating subplots for each of the variables
fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(10, 20))
fig.suptitle('Univariate Analysis of Variables', fontsize=16)

# Analyzing each variable
eps_summary = analyze_variable(df, 'EPS', axes[0])
WIP_summary = analyze_variable(df, 'WIP', axes[1])
block_summary = analyze_variable(df, 'Block', axes[2])
gdppc_summary = analyze_variable(df, 'GDPpc', axes[3])
education_summary = analyze_variable(df, 'Education', axes[4])

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

#Save Figure
path = "/OUT_plots/Alternative/Univariate_Key_Variables.pdf"
plt.savefig(directory + path)
plt.show()

# Displaying summary statistics
univariate_summaries = pd.DataFrame({
    'EPS': eps_summary,
    'WIP': WIP_summary,
    'Block': block_summary,
    'GDPpc': gdppc_summary,
    'Education': education_summary
})

univariate_summaries


"""
*******************************************************************************
MULTIVARIATE ANALYSIS
*******************************************************************************
"""
# Exploring relationships between EPS and other variables

# Correlation matrix to understand the relationships between variables
correlation_matrix = df.corr()

# Pairplot to visualize bivariate relationships
pairplot = sns.pairplot(df, vars=['EPS', 'WIP', 'GDPpc', 'Education'], kind='reg', markers='.')
pairplot.fig.suptitle('Pairplot of Key Variables', fontsize=16)
plt.subplots_adjust(top=0.95)

# Displaying the correlation matrix
correlation_matrix.style.background_gradient(cmap='coolwarm').set_precision(2)
path = "/OUT_plots/Alternative/Pairplot_Key_Variables.pdf"
pairplot.savefig(directory + path)


"""
*******************************************************************************
Regression ANALYSIS
*******************************************************************************
"""
"""
OLS Regression
*******************************************************************************
"""
# Independent variables
X = df[['WIP', 'GDPpc', 'Education']]
# Adding a constant to the model (intercept)
X = sm.add_constant(X)
# Dependent variable
y = df['EPS']
# Rechecking for NaN or infinite values in the independent variables after import correction
nan_indep_vars = X.isna().sum()
inf_indep_vars = np.isinf(X).sum()
# Handling infinite values by replacing them with NaN
X.replace([np.inf, -np.inf], np.nan, inplace=True)
# Dropping rows with NaN values in the independent variables
X_clean = X.dropna()
y_clean = y.loc[X_clean.index]
# Rebuilding the regression model with the cleaned data
model = sm.OLS(y_clean, X_clean).fit()
# Getting the summary of the cleaned regression model
print(model.summary())


"""
>>>OLS Regression with Interaction Term
*******************************************************************************
"""
# Preparing data for regression analysis
# Independent variables
df['WIP_Block_Interaction'] = df['WIP'] * df['Block']

X = df[['WIP', "Block", "WIP_Block_Interaction", 'GDPpc', 'Education']]
# Adding a constant to the model (intercept)
X = sm.add_constant(X)

# Dependent variable
y = df['EPS']

# Rechecking for NaN or infinite values in the independent variables after import correction
nan_indep_vars = X.isna().sum()
inf_indep_vars = np.isinf(X).sum()

# Handling infinite values by replacing them with NaN
X.replace([np.inf, -np.inf], np.nan, inplace=True)

# Dropping rows with NaN values in the independent variables
X_clean = X.dropna()
y_clean = y.loc[X_clean.index]

# Rebuilding the regression model with the cleaned data
model_clean = sm.OLS(y_clean, X_clean).fit()

# Getting the summary of the cleaned regression model
model_clean_summary = model_clean.summary()
model_clean_summary

"""
Regression Including Entity FE
*******************************************************************************
"""
# Preparing the dataset for panel data analysis
# Converting 'CC' (Country Code) and 'Year' to categorical for fixed effects model
df['CC'] = df['CC'].astype('category')
df['Year'] = df['Year'].astype('category')

# Fixed Effects Model
fe_model = smf.ols(formula='EPS ~ WIP + GDPpc + Education + C(CC)', data=df).fit()
# Summaries of the models
fe_model_summary = fe_model.summary()
fe_model_summary


"""
>>>Regression Including Entity and Time FE
*******************************************************************************
"""
# Implementing the Fixed Effects Model including Time Fixed Effects

# Adding year as a categorical variable for time fixed effects
df['Year'] = df['Year'].astype('category')

# Fixed Effects Model with Time Fixed Effects
fe_time_model = smf.ols(formula='EPS ~ WIP + GDPpc + Education + C(CC) + C(Year)', data=df).fit()

# Summary of the model with time fixed effects
fe_time_model_summary = fe_time_model.summary()
fe_time_model_summary


"""
>>>Regression Including Entity and Time FE with Interaction Term
*******************************************************************************
"""
# Implementing the Fixed Effects Model including Time Fixed Effects

# Adding year as a categorical variable for time fixed effects
df['Year'] = df['Year'].astype('category')

# Fixed Effects Model with Time Fixed Effects
fe_time_model = smf.ols(formula='EPS ~ WIP + Block + WIP_Block_Interaction + GDPpc + Education + C(CC) + C(Year)', data=df).fit()

# Summary of the model with time fixed effects
fe_time_model_summary = fe_time_model.summary()
fe_time_model_summary

"""
Difference in Difference - T=SVN, C=HUN
*******************************************************************************
"""
# Select the control group country code (e.g., 'AUT' for Austria)
control_country = 'HUN'
# Create the treatment indicator: 1 for Slovenia, 0 for the control country
df['treatment'] = np.where(df['CC'] == 'SVN', 1, 
                           np.where(df['CC'] == control_country, 0, np.nan))

# Drop all other countries from the analysis
df_did = df.dropna(subset=['treatment'])
df_did['Year'] = pd.to_numeric(df_did['Year'])
# Create the time period indicator: 1 for 2010 and later, 0 for before 2010
df_did['post'] = np.where(df_did['Year'] >= 2010, 1, 0)
# Create the interaction term
df_did['treatment_x_post'] = df_did['treatment'] * df_did['post']
# OLS regression with interaction term
did_model = smf.ols(formula='EPS ~ treatment + post + treatment_x_post + GDPpc + Education', 
                    data=df_did).fit()

# Print the summary of the model
print(did_model.summary())


#Plotting the Findings
sns.lineplot(x='Year', y='EPS', hue='treatment', data=df_did, estimator=np.mean)
plt.title('Average Environmental Policy Stringency (EPS) Over Time')
plt.ylabel('Average EPS')
plt.xlabel('Year')
plt.axvline(x=2010, color='red', linestyle='--', label='Gender Quotas Introduced in 2010 (Slovenia)')
plt.legend(title='Group', labels=['Control', 'Treatment (Slovenia)'])
plt.show()

"""
Statistically, this is often checked by ensuring that the interaction term between the treatment group and the time period (year) 
is not significant in the pre-intervention period. 
This suggests that the rate of change over time in the outcome variable is not significantly different between the two groups before the intervention.

"""
# Statistical Check for Parallel Trends
# For this, we can use a simple OLS regression of EPS on a time trend, treatment, and their interaction
# before 2010 (Pre-intervention period)
df_pre_2010 = df_did[df_did['Year'] < 2010]

# Adding an interaction term between treatment and year
df_pre_2010['treatment_x_year'] = df_pre_2010['treatment'] * df_pre_2010['Year']

# Running the regression
parallel_trends_model = smf.ols('EPS ~ Year + treatment + treatment_x_year', data=df_pre_2010).fit()

# Output the summary of the model
parallel_trends_model_summary = parallel_trends_model.summary()
parallel_trends_model_summary



"""
Difference in Difference - T=SVN, C=Average of CZR, POL, HUN
*******************************************************************************
"""
control_countries = ['CZR', 'POL', 'HUN']
control_df = df[df['CC'].isin(control_countries)]
control_avg = control_df.groupby('Year').mean().reset_index()
control_avg['CC'] = 'AVG_CONTROL'
df = df.append(control_avg, ignore_index=True)
# Create the treatment indicator: 1 for Slovenia, 0 for the average control country
df['treatment'] = np.where(df['CC'] == 'SVN', 1, 
                           np.where(df['CC'] == 'AVG_CONTROL', 0, np.nan))

df_did = df.dropna(subset=['treatment'])
df_did['Year'] = pd.to_numeric(df_did['Year'])

# Create the time period indicator: 1 for 2010 and later, 0 for before 2010
df_did['post'] = np.where(df_did['Year'] >= 2010, 1, 0)
df_did['treatment_x_post'] = df_did['treatment'] * df_did['post']
# OLS regression
did_model = smf.ols(formula='EPS ~ treatment + post + treatment_x_post + GDPpc + Education', 
                    data=df_did, cov_type='cluster').fit()
# Output the results
print(did_model.summary())




# Statistical Check for Parallel Trends
# For this, we can use a simple OLS regression of EPS on a time trend, treatment, and their interaction
# before 2010 (Pre-intervention period)
df_pre_2010 = df_did[df_did['Year'] < 2010]
# Adding an interaction term between treatment and year
df_pre_2010['treatment_x_year'] = df_pre_2010['treatment'] * df_pre_2010['Year']
# Running the regression
parallel_trends_model = smf.ols('EPS ~ Year + treatment + treatment_x_year', data=df_pre_2010).fit()
# Output the summary of the model
parallel_trends_model_summary = parallel_trends_model.summary()
parallel_trends_model_summary




#Plotting the Findings
palette = {"SVN": "orange", "AVG_CONTROL": "purple"}
sns.lineplot(x='Year', y='EPS', hue='CC', data=df_did, estimator=np.mean, palette=palette)
plt.title('Average Environmental Policy Stringency (EPS) Over Time')
plt.ylabel('Average EPS')
plt.xlabel('Year')
plt.axvline(x=2010, color='red', linestyle='--')
plt.xticks(ticks=range(2000, 2021, 5))
handles, labels = plt.gca().get_legend_handles_labels()
quota_line = mlines.Line2D([], [], color='red', linestyle='--', label='Quota Introduced')
handles.append(quota_line)
labels.append('Quota Introduced')
plt.legend(handles=handles, labels=labels, title='', loc='lower right')
path = "/OUT_plots/DID_AVG.pdf"
plt.savefig(directory + path)
plt.show()



#DiD 1
control_country = 'HUN'
df['treatment'] = np.where(df['CC'] == 'SVN', 1,
                           np.where(df['CC'] == control_country, 0, np.nan))

df_did = df.dropna(subset=['treatment'])
df_did['Year'] = pd.to_numeric(df_did['Year'])
df_did['post'] = np.where(df_did['Year'] >= 2010, 1, 0)
df_did['treatment_x_post'] = df_did['treatment'] * df_did['post']
did_model = smf.ols(formula='EPS ~ treatment + post + treatment_x_post + GDPpc + Education',
                    data=df_did).fit()

#Plot
palette = {"SVN": "orange", "HUN": "purple"}
plt.figure(figsize=(8, 6))
sns.lineplot(x='Year', y='EPS', hue='CC', data=df_did, estimator=np.mean, palette=palette)
plt.title('Average Environmental Policy Stringency (EPS) Over Time')
plt.ylabel('Average EPS')
plt.xlabel('Year')
plt.axvline(x=2010, color='red', linestyle='--')
plt.xticks(ticks=range(2000, 2021, 5))
handles, labels = plt.gca().get_legend_handles_labels()
quota_line = mlines.Line2D([], [], color='red', linestyle='--', label='Quota Introduced')
handles.append(quota_line)
labels.append('Quota Introduced')
plt.legend(handles=handles, labels=labels, title='', loc='lower right')
path = "/OUT_plots/DID_HUN.pdf"
plt.savefig(directory + path)
plt.show()