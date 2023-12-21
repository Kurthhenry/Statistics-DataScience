#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 17:30:27 2023

@author: timbaettig
"""

import pandas as pd

"""
*******************************************************************************
Preliminary Specifications
*******************************************************************************
"""

directory = "/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data"

df = pd.read_csv('/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OECD/OECD_EPS.csv', index_col=False)
df['Country'] = df['Country'].replace('Türkiye', 'Turkey')

#specification of year range 
year_range = list(range(1990,2021))
year_range_2 = list(range(2000,2021))
short_range = list(range(1985,1997))

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

countrymap = {"Greece":"GRC",
"Portugal":"PRT",
"France":"FRA",
"Belgium":"BEL",
"Switzerland":"CHE",
"Czech Republic":"CZE",
"Denmark":"DNK",
"Italy":"ITA",
"Spain":"ESP",
"Sweden":"SWE",
"United Kingdom":"GBR",
"Poland":"POL",
"Netherlands":"NLD",
"Ireland":"IRL",
"Finland":"FIN",
"Hungary":"HUN",
"Germany":"DEU",
"Norway":"NOR",
"Slovak Republic":"SVK",
"Austria":"AUT",
"Turkey":"TUR",
"Slovenia":"SVN",
"Russia":"RUS"}

"""
#west=0, neutral=1, east=2
eastwestmap = {"Greece":0,
"Portugal":0,
"France":0,
"Belgium":0,
"Switzerland":1,
"Czech Republic":2,
"Denmark":0,
"Italy":0,
"Spain":0,
"Sweden":1,
"United Kingdom":0,
"Poland":2,
"Netherlands":0,
"Ireland":1,
"Finland":1,
"Hungary":2,
"Germany":0,
"Norway":0,
"Slovak Republic":2,
"Austria":1,
"Turkey":0,
"Slovenia":2,
"Russia":2}"""

#west=0, east=1
eastwestmap = {"Greece":0,
"Portugal":0,
"France":0,
"Belgium":0,
"Switzerland":0,
"Czech Republic":1,
"Denmark":0,
"Italy":0,
"Spain":0,
"Sweden":0,
"United Kingdom":0,
"Poland":1,
"Netherlands":0,
"Ireland":0,
"Finland":0,
"Hungary":1,
"Germany":0,
"Norway":0,
"Slovak Republic":1,
"Austria":0,
"Turkey":0,
"Slovenia":1,
"Russia":1}

west = ["GRC", "PRT", "FRA", "BEL", "DEN", "ITA", "ESP", "GBR", "NLD", "DEU", "NOR", "TUR"]
east = ["CZE", "POL", "HUN", "SVK", "SVN", "RUS"]

"""
*******************************************************************************
Data Cleaning and Preparation
*******************************************************************************
"""
#Dataframe: Environmental Policy Stringency
dfeps = df
dfeps = dfeps.loc[dfeps['Country'].isin(countrylist)]
dfeps = dfeps.loc[dfeps['VAR'] == "EPS"]
dfeps = dfeps.drop(["Country","VAR","Variable", "YEA", "Unit Code", "Unit", "PowerCode Code", "PowerCode", "Reference Period Code", "Reference Period", "Flag Codes", "Flags"], axis=1)
dfeps.rename(columns={'COU': 'CC'}, inplace=True)
dfeps.rename(columns={'Value': 'EPS'}, inplace=True)
dfeps = dfeps.loc[dfeps['Year'].isin(year_range_2)]

#test sample size: 
obs_eps = list(dfeps["CC"].unique())
#Export
path = "/OUT_df/EPS_cleaned.csv"
dfeps.to_csv(directory + path, index=False)


#women in parliament dataframe (UIP)
dfww = pd.read_excel("/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/IPU/WIP_IPU.xlsx")
dfww = dfww.drop(["Region", "Election / Renewal", "Month", "Chamber Total Seats", "Total women"], axis=1)
dfww['Country'] = dfww['Country'].replace('Slovakia', 'Slovak Republic')
dfww = dfww.loc[dfww['Country'].isin(countrylist)]
#obs_WIP = list(dfww["Country"].unique())
dfww = dfww[dfww['Chamber Type'] != 'Upper']
dfww = dfww.drop(["Chamber Type", "NOTES"], axis=1)
dfww.rename(columns={'% Of Women in Chamber': 'WIP'}, inplace=True)
dfww = dfww.loc[dfww['Year'].isin(short_range)]

all_years_countries = pd.DataFrame([(year, country) for year in range(1985, 1997) for country in countrylist], columns=['Year', 'Country'])
merged_df = all_years_countries.merge(dfww, on=['Year', 'Country'], how='left')
merged_df['WIP'] = merged_df.groupby('Country')['WIP'].fillna(method='ffill')
dfww = merged_df
dfww = dfww.loc[dfww['Year'].isin(year_range)]
dfww['Country'] = dfww['Country'].map(countrymap)
neworder = ['Country', 'Year', 'WIP']
dfww = dfww[neworder]
dfww.rename(columns={'Country': 'CC'}, inplace=True)
dfww['WIP'] = dfww['WIP'] * 100

#second WIP dataframe
dfw = pd.read_csv("/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OurWorldInData/womeninparliament.csv")
#dfw["Code"].unique()
dfw.rename(columns={'Code': 'CC'}, inplace=True)
dfw.rename(columns={'Proportion of seats held by women in national parliaments (%)': 'WIP'}, inplace=True)
dfw = dfw.drop("Entity", axis=1)
dfw = dfw.loc[dfw['CC'].isin(cclist)]

#Merging the two dataframes
dfw_merged = pd.concat([dfw, dfww])
dfw_merged = dfw_merged.sort_values(by=['CC',"Year"])
dfw_merged = dfw_merged.reset_index(drop=True)
dfw_merged["WIP"] = dfw_merged["WIP"].astype(float)
dfw_merged = dfw_merged.loc[dfw_merged['Year'].isin(year_range_2)]
#obs_WIP = list(dfw_merged["CC"].unique())
#Export
path = "/OUT_df/Share_WIP_Cleaned.csv"
dfw_merged.to_csv(directory + path, index=False)


# dataframe for east - west blocks
dfew = pd.DataFrame(list(eastwestmap.items()), columns=['Country', 'Block'])
for year in range(1990, 2022):
    dfew[str(year)] = dfew['Block']
    
dfew.drop('Block', axis=1, inplace=True)
dfew = pd.melt(dfew, id_vars=['Country'], var_name='Year', value_name='Block')
dfew['Country'] = dfew['Country'].map(countrymap)
dfew.rename(columns={'Country': 'CC'}, inplace=True)
dfew = dfew.sort_values(by=['CC',"Year"])
dfew = dfew.reset_index(drop=True)
dfew["Year"] = dfew["Year"].astype(int)
dfew = dfew.loc[dfew['Year'].isin(year_range_2)]
#obs_ew = list(dfew["CC"].unique())
path = "/OUT_df/east_west_cleaned.csv"
dfew.to_csv(directory + path, index = False)


# dataframe for GDP
dfg = pd.read_csv("/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OECD/GDP_pc.csv")
dfg = dfg.drop(["INDICATOR", "SUBJECT", "MEASURE", "FREQUENCY", "Flag Codes"], axis=1)
dfg.rename(columns={'LOCATION': 'CC', "TIME":"Year", "Value":"GDPpc"}, inplace=True)
dfg = dfg.loc[dfg['CC'].isin(cclist)]
dfg = dfg.loc[dfg['Year'].isin(year_range_2)]
path = "/OUT_df/GDPpc_cleaned.csv"
dfg.to_csv(directory + path, index = False)

# dataframe for Education
dfe = pd.read_csv("/Users/timbaettig/Library/Mobile Documents/com~apple~CloudDocs/00_Privat/00_EPFL/Courses/AS 2023/Statistics and Data Science/Paper/Data/OECD/Education.csv")
dfe = dfe.drop(["INDICATOR", "SUBJECT", "MEASURE", "FREQUENCY", "Flag Codes"], axis=1)
dfe.rename(columns={'LOCATION': 'CC', "TIME":"Year", "Value":"Education"}, inplace=True)
dfe = dfe.loc[dfe['CC'].isin(cclist)]

dfe_pivot = dfe.pivot(index='Year', columns='CC', values="Education").reset_index()
dfe_pivot = dfe_pivot.fillna(method='bfill')
dfe_pivot = dfe_pivot.fillna(method='ffill')
dfe = pd.melt(dfe_pivot, id_vars=['Year'], var_name='CC', value_name='Education')
dfe = dfe.loc[dfe['Year'].isin(year_range_2)]
neworder = ['CC', 'Year', "Education"]
dfe = dfe[neworder]
path = "/OUT_df/education_cleaned.csv"
dfe.to_csv(directory + path, index = False)


#LAST STEP
#merging the dataframes
dfew['Year'] = dfew['Year'].astype(int)
merged = dfeps.merge(dfew, on=['CC', 'Year'])
merged = merged.merge(dfw_merged, on=["CC", "Year"], how= "outer")
merged = merged.merge(dfg, on=["CC", "Year"], how= "outer")
merged = merged.merge(dfe, on=["CC", "Year"], how= "outer")
merged = merged[merged['Year'] != 2021]
merged = merged[merged['Year'] != 2022]
merged = merged.sort_values(by=['CC',"Year"])
merged["WIP"] = merged["WIP"].fillna(method='bfill')
neworder = ['CC', 'Year', 'EPS', "WIP", "Block", "GDPpc", "Education"]
merged = merged[neworder]

#merged["Education"] = merged["Education"].fillna(method='bfill')

#export
path = "/OUT_df/final_df_cleaned.csv"
merged.to_csv(directory + path, index = False)