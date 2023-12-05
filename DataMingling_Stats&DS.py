#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 17:35:14 2023

@author: timbaettig
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns


"""
Data Cleaning and Preparation
*******************************************************************************
"""

directory = "/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data"
#Getting an Overview
df = pd.read_csv('/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OECD/OECD_EPS.csv', index_col=False)
df.head()
dfger = df.loc[df['Country'] == "Germany"]
dfger = dfger.drop(['Country', "YEA", "Unit Code", "Unit", "PowerCode Code", "PowerCode", "Reference Period Code", "Reference Period", "Flag Codes", "Flags"], axis=1)

"""
#Specification of Countries 
lis = list(df["Country"].unique())
lis.remove("Japan")
lis.remove("United States")
lis.remove("Canada")
lis.remove("Korea")
lis.remove("Australia")
lis.remove("South Africa")
lis.remove("China (People's Republic of)")
lis.remove("Indonesia")
lis.remove("Brazil")
lis.remove("India")
countrylist = lis
"""

#specification of 3l-CC
lis = list(df["COU"].unique())
lis.remove("JPN")
lis.remove("USA")
lis.remove("CAN")
lis.remove("KOR")
lis.remove("AUS")
lis.remove("ZAF")
lis.remove("CHN")
lis.remove("IDN")
lis.remove("BRA")
lis.remove("IND")
cclist = lis

#specification of year range 
year_range = list(range(1990,2021))

#Environmental Policy Stringency dataframe
oecd_df = df.loc[df['COU'].isin(cclist)]
oecd_df = oecd_df.loc[df['VAR'] == "EPS"]
oecd_df = oecd_df.drop(["VAR","Variable","Country", "YEA", "Unit Code", "Unit", "PowerCode Code", "PowerCode", "Reference Period Code", "Reference Period", "Flag Codes", "Flags"], axis=1)
oecd_df.rename(columns={'COU': 'CC'}, inplace=True)
oecd_df.rename(columns={'Value': 'EPS'}, inplace=True)
#Export
path = "/OUT_df/EPS_cleaned.csv"
oecd_df.to_csv(directory + path, index=False)

#women in parliament dataframe
dfw = pd.read_csv("/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OurWorldInData/womeninparliament.csv")
#dfw["Code"].unique()
dfw.rename(columns={'Code': 'CC'}, inplace=True)
dfw.rename(columns={'Proportion of seats held by women in national parliaments (%)': 'Share WiP'}, inplace=True)
dfw = dfw.drop("Entity", axis=1)
dfw = dfw.loc[dfw['CC'].isin(cclist)]
#Export
path = "/OUT_df/Share_WiP_Cleaned.csv"
dfw.to_csv(directory + path, index=False)

#demographics dataframe
dfg = pd.read_csv("/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/WB/perc_urban_pop.csv")
dfg = dfg.drop("Unnamed: 67", axis=1)
dfg.rename(columns={'Country Code': 'CC'}, inplace=True)
dfg = dfg.loc[dfg['CC'].isin(cclist)]
dfg = dfg.drop(["Country Name", "Indicator Name", "Indicator Code"], axis=1)
dfg = dfg.melt(id_vars=['CC'], var_name='Year', value_name='Share UPop')
#test = list(dfg["CC"].unique())
#Export
path = "/OUT_df/Share_UPop_Cleaned.csv"
dfg.to_csv(directory + path, index = False)

#merging the dataframes
dfg['Year'] = dfg['Year'].astype(int)
merged = oecd_df.merge(dfg, on=['CC', 'Year'])
merged = merged.merge(dfw, on=["CC", "Year"], how= "outer")
merged = merged[merged['Year'] != 2021]
#export
path = "/OUT_df/final_df_cleaned.csv"
merged.to_csv(directory + path, index = False)


"""
Computation of Summary Statistics
*******************************************************************************
"""
"""Some summary statistics"""
#average share of women in parliament
means_wip = dfw.groupby(dfw["CC"])['Share WiP'].mean().reset_index()
means_wip.rename(columns={'Share WiP': 'Average Share WiP'}, inplace=True)
means_wip = means_wip.sort_values(by='Average Share WiP', ascending = False)

#average eps score
means_eps = oecd_df.groupby(oecd_df["CC"])['EPS'].mean().reset_index()
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
summary_stats = summary_stats[['Statistic', 'EPS', 'Share WiP', "Share UPop"]]

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
with open('table.tex', 'w') as f:
    f.write(latex_document)

"""
Correlation Table
*******************************************************************************
"""
corr = merged.corr()
#heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='plasma', vmin=-1, vmax=1)
plt.title('Correlation Table Heatmap')
path = "/OUT_plots/Correlation_Heatmap.pdf"
plt.savefig(directory + path)
plt.show()

"""
Visualisations
*******************************************************************************
"""
"""Scatter Plot to Identify Outliers"""
#EPS - WiP
plt.scatter(merged['EPS'], merged['Share WiP'], c=merged['Share WiP'], cmap='cividis', marker='o')
plt.colorbar(label='% Share')
plt.xlabel('Environmental Policy Stringency')
plt.ylabel('Share of Women in Parliament')
plt.title("Distribution of Values for EPS Score and Women in Parliament")
path = "/OUT_plots/Scatter_EPS_WiP.pdf"
plt.savefig(directory + path)
plt.show()

#EPS - UPop
plt.scatter(merged['EPS'], merged['Share UPop'], c=merged['Share UPop'], cmap='viridis', marker='o')
plt.colorbar(label='% Share')
plt.xlabel('Environmental Policy Stringency')
plt.ylabel('Share of Urban Population')
plt.title("Distribution of Values for EPS Score and Urban Population Share")
path = "/OUT_plots/Scatter_EPS_UPop.pdf"
plt.savefig(directory + path)
plt.show()

"""Some Bar Plots to Show Macro Trends"""
#barplot for average share of women in parliament
categories = means_wip["CC"]
values = means_wip["Average Share WiP"]
# Create a colormap
colormap = plt.cm.get_cmap('cividis')
# Normalize values to the range [0, 1]
normalize = plt.Normalize(vmin=min(values), vmax=max(values))
# Create a figure and axis
fig, ax = plt.subplots()
# Plot the bars with gradient colors
bars = plt.bar(categories, values, color=colormap(normalize(values)))
# Add labels and a title
plt.xlabel('Country')
plt.xticks(rotation=90)
plt.ylabel('Share in %')
plt.title('Avergae Share of Women in Parliament by Country')

path = "/OUT_plots/Average_Share_WiP.pdf"
plt.savefig(directory + path)
plt.show()

#barplot for average EPS scores
categories = means_eps["CC"]
values = means_eps["Average EPS"]
# Create a colormap
colormap = plt.cm.get_cmap('viridis')
# Normalize values to the range [0, 1]
normalize = plt.Normalize(vmin=min(values), vmax=max(values))
# Create a figure and axis
fig, ax = plt.subplots()
# Plot the bars with gradient colors
bars = plt.bar(categories, values, color=colormap(normalize(values)))
# Add labels and a title
plt.xlabel('Country')
plt.xticks(rotation=90)
plt.ylabel('Environmental Policy Stringency Score')
plt.title('Average Stringency of Environmental Policy by Country')
"""
# Add a colorbar
sm = plt.cm.ScalarMappable(cmap=colormap, norm=normalize)
sm.set_array([])  # This line is needed to properly scale the colorbar
plt.colorbar(sm, label='Color Intensity')
"""
path = "/OUT_plots/Average_EPS.pdf"
plt.savefig(directory + path)
plt.show()

"""lineplots to show the evolution of the variables over time"""
#development of WiP
dfw_pivot = dfw.pivot(index='Year', columns='CC', values="Share WiP")
avg_dfw = dfw.groupby('Year')['Share WiP'].mean().reset_index()
dfw_pivot = dfw_pivot.merge(avg_dfw, on= "Year")
dfw_pivot = dfw_pivot[dfw_pivot['Year'] != 2021]
dfw_pivot = dfw_pivot.set_index('Year')
dfw_pivot.rename(columns={'Share WiP': 'Average'}, inplace=True)
highlight_country = 'Average'
highlight_color = "yellow"
ax = plt.gca()  # Get current axis
for country in dfw_pivot.columns:
    if country == highlight_country:
        dfw_pivot[country].plot(ax=ax, color=highlight_color, label=country, linewidth=4)
    else:
        dfw_pivot[country].plot(ax=ax, color='grey', label='_nolegend_')
#plt.xticks([1990, 1995, 2000, 2005, 2010, 2015, 2020])
plt.title("Trends in Women's Share in Parliament")
plt.ylabel('% Share')
plt.xlabel('Year')
#plt.grid(True)
plt.legend()
path = "/OUT_plots/Line_WiP_wAverage.pdf"
plt.savefig(directory + path)
plt.show()

#development of UPop
dfg_pivot = dfg.pivot(index='Year', columns='CC', values="Share UPop")
avg_dfg = dfg.groupby('Year')['Share UPop'].mean().reset_index()
dfg_pivot = dfg_pivot.merge(avg_dfg, on= "Year")
dfg_pivot = dfg_pivot[(dfg_pivot['Year'] >= 1990) & (dfg_pivot['Year'] <= 2020)]
dfg_pivot = dfg_pivot.set_index('Year')
dfg_pivot.rename(columns={'Share UPop': 'Average'}, inplace=True)
highlight_country = 'Average'
highlight_color = 'lightgreen'
ax = plt.gca()  # Get current axis
for country in dfg_pivot.columns:
    if country == highlight_country:
        dfg_pivot[country].plot(ax=ax, color=highlight_color, label=country, linewidth=4)
    else:
        dfg_pivot[country].plot(ax=ax, color='grey', label='_nolegend_') 
plt.title("Trends in Urban Population Shares")
plt.ylabel('% Share')
plt.xlabel('Year')
#plt.grid(True)
plt.legend()
path = "/OUT_plots/Line_UPop_wAverage.pdf"
plt.savefig(directory + path)
plt.show()

#development of EPS
dfe_pivot = oecd_df.pivot(index='Year', columns='CC', values="EPS")
avg_dfe = oecd_df.groupby('Year')['EPS'].mean().reset_index()
dfe_pivot = dfe_pivot.merge(avg_dfe, on= "Year")
dfe_pivot = dfe_pivot.set_index('Year')
dfe_pivot.rename(columns={'EPS': 'Average'}, inplace=True)
highlight_country = 'Average'
highlight_color = 'blue'
ax = plt.gca()  # Get current axis
for country in dfe_pivot.columns:
    if country == highlight_country:
        dfe_pivot[country].plot(ax=ax, color=highlight_color, label=country, linewidth=4)
    else:
        dfe_pivot[country].plot(ax=ax, color='grey', label='_nolegend_') 
plt.title("Trends in Environmental Policy Stringency")
plt.ylabel('EPS Score')
plt.xlabel('Year')
#plt.grid(True)
plt.legend()
path = "/OUT_plots/Line_EPS_wAverage.pdf"
plt.savefig(directory + path)
plt.show()
