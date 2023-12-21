#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 12:02:30 2023

@author: timbaettig
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.patches as mpatches

directory = "/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data"
merged = pd.read_csv('/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OUT_df/final_df_cleaned.csv', index_col=False)
dfw_merged = pd.read_csv('/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OUT_df/Share_WIP_Cleaned.csv', index_col=False)
dfeps = pd.read_csv('/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OUT_df/EPS_cleaned.csv', index_col=False)

west = ["GRC", "PRT", "FRA", "BEL", "DEN", "ITA", "ESP", "GBR", "NLD", "DEU", "NOR", "TUR"]
east = ["CZE", "POL", "HUN", "SVK", "SVN", "RUS"]

"""
*******************************************************************************
Univariate Analysis
*******************************************************************************
"""
#Summary Statistics
#average share of women in parliament
means_WIP = dfw_merged.groupby(dfw_merged["CC"])['WIP'].mean().reset_index()
means_WIP.rename(columns={'WIP': 'Average WIP'}, inplace=True)
means_WIP = means_WIP.sort_values(by='Average WIP', ascending = False)

#average eps score
means_eps = dfeps.groupby(dfeps["CC"])['EPS'].mean().reset_index()
means_eps.rename(columns={'EPS': 'Average EPS'}, inplace=True)
means_eps = means_eps.sort_values(by='Average EPS', ascending = False)

summary_stats = merged.describe()
new_labels = {
    'count': 'Number of Observations',
    'mean': 'Mean',
    'std': 'Standard Deviation',
    'min': 'Minimum Value',
    '25%': '1st Quartile',
    '50%': 'Median',
    '75%': '3rd Quartile',
    'max': 'Maximum Value'
}
summary_stats = summary_stats.rename(index=new_labels)
summary_stats = summary_stats.reset_index()
summary_stats = summary_stats.drop("Year", axis=1)
summary_stats.rename(columns={'index': 'Statistic'}, inplace=True)
summary_stats = summary_stats.round(2)
summary_stats = summary_stats[['Statistic', 'EPS', 'WIP', "Block", "GDPpc", "Education"]]
print(summary_stats)

#table export to LaTeX format -> tbc in Overleaf
latex_ss = summary_stats.to_latex(index=False)
latex_document = r"""
\documentclass{article}
\begin{document}
\begin{table}
\centering
""" + latex_ss + r"""
\caption{Sample table}
\end{table}
\end{document}
"""
with open('/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OUT_tables/table.tex', 'w') as f:
    f.write(latex_document)



#Visualisation of Summary Statistics
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
eps_summary = analyze_variable(merged, 'EPS', axes[0])
WIP_summary = analyze_variable(merged, 'WIP', axes[1])
block_summary = analyze_variable(merged, 'Block', axes[2])
gdppc_summary = analyze_variable(merged, 'GDPpc', axes[3])
education_summary = analyze_variable(merged, 'Education', axes[4])

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

#Save Figure
path = "/OUT_plots/Univariate_Key_Variables.pdf"
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


#Pie plot for block distirbution
counts = [sum(merged["Block"] == 0), sum(merged["Block"] == 1)]
plt.pie(counts, labels=['West', 'East'], autopct='%1.1f%%')
plt.title("Distribution of East/West Observations")
path = "/OUT_plots/Pie_Block.pdf"
plt.savefig(directory + path)
plt.show()


"""
*******************************************************************************
Bivariate Analysis
*******************************************************************************
"""
"""Correlation Tables"""

"""Heatmap"""
corr = merged.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='plasma', vmin=-1, vmax=1)
plt.title('Correlation Table Heatmap')
path = "/OUT_plots/Correlation_Heatmap.pdf"
plt.savefig(directory + path)
plt.show()

#Distributions
# Exploring relationships between EPS and other variables

"""Pair Plots"""
# Correlation matrix to understand the relationships between variables
correlation_matrix = merged.corr()

# Pairplot to visualize bivariate relationships
pairplot = sns.pairplot(merged, vars=['EPS', 'WIP', 'GDPpc', 'Education'], kind='reg', markers='.')
pairplot.fig.suptitle('Pairplot of Key Variables', fontsize=16)
plt.subplots_adjust(top=0.95)

# Displaying the correlation matrix
correlation_matrix.style.background_gradient(cmap='coolwarm').set_precision(2)
path = "/OUT_plots/Pairplot_Key_Variables.pdf"
pairplot.savefig(directory + path)


"""Scatter Plots"""
color_map = {0: 'blue', 1: 'red'}
colors = merged['Block'].apply(lambda x: color_map.get(x, 'black'))  # 'black' for any unexpected value

# Create a figure and a set of subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 6))  # Adjust figsize as needed

# Create legend handles
west_patch = mpatches.Patch(color='blue', label='West')
east_patch = mpatches.Patch(color='red', label='East')

# Define the subplots
for i, (col, title) in enumerate(zip(['WIP', 'GDPpc', 'Education'], 
                                     ['% Share of Women in Parliament', 
                                      'GDP per capita', 
                                      '% of Population with Tertiary Education'])):
    slope, intercept = np.polyfit(merged[col], merged['EPS'], 1)
    axes[i].scatter(merged[col], merged['EPS'], c=colors, marker='o')
    y_fit = slope * np.array(merged[col]) + intercept
    axes[i].plot(merged[col], y_fit, color='green')
    axes[i].set_xlabel(title)
    axes[i].set_ylabel('Environmental Policy Stringency')

# Set the titles
titles = ["Distribution of Values for EPS Score and Women in Parliament",
          "Distribution of Values for EPS Score and GDP Per Capita",
          "Distribution of Values for EPS Score and Tertiary Education"]
for ax, title in zip(axes, titles):
    ax.set_title(title)

# Add the legend to the first subplot
axes[0].legend(handles=[west_patch, east_patch], loc="upper left")

# Adjust layout
plt.tight_layout()

# Save the combined plot
path = "/OUT_plots/Scatter_EPS_Combined.pdf"
plt.savefig(directory + path)

# Show the plot
plt.show()


"""Lineplots"""
#development of WIP
dfw_pivot = dfw_merged.pivot(index='Year', columns='CC', values="WIP")
dfw_pivot = dfw_pivot.fillna(method='bfill')
dfw_pivot.rename(columns={'WIP': 'Average'}, inplace=True)
highlight_country = 'SVN'
highlight_color = "black"
ax = plt.gca()  # Get current axis
for country in dfw_pivot.columns:
    if country == highlight_country:
        dfw_pivot[country].plot(ax=ax, color=highlight_color, label=country, linewidth=4)
    elif country in east:
        dfw_pivot[country].plot(ax=ax, color='red', label='_nolegend_')
    elif country in west:
        dfw_pivot[country].plot(ax=ax, color='blue', label='_nolegend_')
    else:
        dfw_pivot[country].plot(ax=ax, color='grey', label='_nolegend_')
plt.xticks([2000, 2005, 2010, 2015, 2020])
plt.title("Trends in Women's Share in Parliament")
plt.ylabel('% Share')
plt.xlabel('Year')
#plt.grid(True)
plt.legend()
path = "/OUT_plots/Line_WIP_wHighlight.pdf"
plt.savefig(directory + path)
plt.show()

#development of EPS
dfeps_pivot = dfeps.pivot(index='Year', columns='CC', values="EPS")
dfeps_pivot.rename(columns={'EPS': 'Average'}, inplace=True)
highlight_country = 'SVN'
highlight_color = 'black'
ax = plt.gca()  # Get current axis
for country in dfeps_pivot.columns:
    if country == highlight_country:
        dfeps_pivot[country].plot(ax=ax, color=highlight_color, label=country, linewidth=4)
    elif country in east:
        dfeps_pivot[country].plot(ax=ax, color='red', label='_nolegend_')
    elif country in west:
        dfeps_pivot[country].plot(ax=ax, color='blue', label='_nolegend_')
    else:
        dfeps_pivot[country].plot(ax=ax, color='grey', label='_nolegend_') 
plt.xticks([2000, 2005, 2010, 2015, 2020])
plt.title("Trends in Environmental Policy Stringency")
plt.ylabel('EPS Score')
plt.xlabel('Year')
#plt.grid(True)
plt.legend()
path = "/OUT_plots/Line_EPS_wHighlight.pdf"
plt.savefig(directory + path)
plt.show()