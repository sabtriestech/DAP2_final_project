import os
import pandas as pd
import numpy as np
import pyreadstat
import geopandas as gpd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
BASE_DIR

os.chdir(BASE_DIR)

# Here we will being to pull in and clean yearly crime data to eventually merge with the main Chetty-Hendren Data
file_path = 'data/crime_data/FBI_Crime_Data'

#importing all my data files and adding year column
crime_2024 = pd.read_excel(f'{file_path}/2024.xlsx',
                            skiprows=4, skipfooter=2)
crime_2024["Year"] = 2024
crime_2023 = pd.read_excel(f'{file_path}/2023.xlsx',
                            skiprows=4, skipfooter=2, index_col=[0]).reset_index()
crime_2023["Year"] = 2023
crime_2022 = pd.read_excel(f'{file_path}/2022.xlsx',
                            skiprows=4, skipfooter=2, index_col=[0]).reset_index()
crime_2022["Year"] = 2022
crime_2021 = pd.read_excel(f'{file_path}/2021.xlsx',
                            skiprows=4, skipfooter=1, index_col=[0]).reset_index()
crime_2021["Year"] = 2021
crime_2020 = pd.read_excel(f'{file_path}/2020.xlsx',
                            skiprows=6, skipfooter=9, index_col=[0]).reset_index()
crime_2020["Year"] = 2020
# for files 2019 and before, these are xls, so user will need to install xlrd in terminal
crime_2019 = pd.read_excel(f'{file_path}/2019.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index() 
crime_2019["Year"] = 2019
crime_2018 = pd.read_excel(f'{file_path}/2018.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index()
crime_2018["Year"] = 2018 
crime_2017 = pd.read_excel(f'{file_path}/2017.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index() 
crime_2017["Year"] = 2017 
crime_2016 = pd.read_excel(f'{file_path}/2016.xls',
                            skiprows=4, skipfooter=9, index_col=[0]).reset_index() 
crime_2016["Year"] = 2016
crime_2015 = pd.read_excel(f'{file_path}/2015.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index()
crime_2015["Year"] = 2015 
crime_2014 = pd.read_excel(f'{file_path}/2014.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index()
crime_2014["Year"] = 2014
crime_2013 = pd.read_excel(f'{file_path}/2013.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index() 
crime_2013["Year"] = 2013
crime_2012 = pd.read_excel(f'{file_path}/2012.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index() 
crime_2012["Year"] = 2012 
crime_2011 = pd.read_excel(f'{file_path}/2011.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index() 
crime_2011["Year"] = 2011
crime_2010 = pd.read_excel(f'{file_path}/2010.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index()
crime_2010["Year"] = 2010 
crime_2009 = pd.read_excel(f'{file_path}/2009.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index()
crime_2009["Year"] = 2009 
crime_2008 = pd.read_excel(f'{file_path}/2008.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index()
crime_2008["Year"] = 2008
crime_2007 = pd.read_excel(f'{file_path}/2007.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index()
crime_2007["Year"] = 2007
crime_2006 = pd.read_excel(f'{file_path}/2006.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index() 
crime_2006["Year"] = 2006
crime_2005 = pd.read_excel(f'{file_path}/2005.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index() 
crime_2005["Year"] = 2005

all_sheets = [crime_2024, crime_2023, crime_2022, crime_2021, crime_2020, crime_2019, crime_2018,
               crime_2017, crime_2016, crime_2015, crime_2014, crime_2013, 
               crime_2012, crime_2011, crime_2010, crime_2009, crime_2008, 
               crime_2007, crime_2006, crime_2005]
# but for all sheets we want to
for s in all_sheets:
    #get rid of line breaks in column headings
    s.columns = s.columns.str.replace('\n', ' ', regex=True)
    #remove footnote from Arson and Rape Column; rename columns that have inconsistent spacing
    s.rename(columns={'Arson1': 'Arson', 'Arson3': 'Arson', 'Arson2': 'Arson', 'Rape1':'Rape',
                       'Metropolitan/Nonmetropolitan': 'County Type', 'Larceny- theft': 'Larceny-theft',
                       'Forcible Rape': 'Rape', 'Forcible  Rape': 'Rape', 'Forcible rape': 'Rape',
                       'Motor  vehicle  theft':'Motor vehicle theft','Motor Vehicle Theft':'Motor vehicle theft',
                       'Murder and  nonnegligent  manslaughter': 'Murder and nonnegligent manslaughter', 
                       'Rape (revised  definition)1': 'Rape (revised definition)1', 
                       'Aggravated  assault': 'Aggravated assault', 'Property  crime': 'Property crime',
                       'Motor  vehicle  theft': 'Motor vehicle theft', 'Violent Crime': 'Violent crime',
                       'Property Crime': 'Property crime', 'Violent  crime':'Violent crime',
                       'Forcible  rape': 'Rape', 'Violent  Crime': 'Violent crime', 
                       'Property  Crime': 'Property crime'}, inplace=True)
    #some states and counties have footnotes at the end that will mean that they won't merge correctly
    s['County'] = s['County'].str.rstrip()
    s['County'] = s['County'].str.replace(r'\s*\d+$', '', regex=True)
    s['State'] = s['State'].str.replace(r'\s*\d+$', '', regex=True)
    #make state titlecase
    s['State'] = s['State'].str.title()

#now to split state name from county type
county_dash = [crime_2023, crime_2022, crime_2021, crime_2019, crime_2018,
               crime_2017, crime_2016, crime_2015, crime_2014, crime_2013, 
               crime_2012, crime_2011, crime_2010, crime_2009, crime_2008, 
               crime_2007, crime_2006, crime_2005]
for c in county_dash: 
    c[['State', 'County Type']] = c['State'].str.split('-', n=1, expand=True)

# In 2013-2016 states have slightly different definitions of Rape, 
# We want to combine these numbers to get total count and then drop the old columns
dif_def = [crime_2013, crime_2014, crime_2015, crime_2016]

for d in dif_def: 
    d['Rape'] = d['Rape (revised definition)1'].fillna(0) + d['Rape (legacy definition)2'].fillna(0)
    d.drop(columns=['Rape (revised definition)1','Rape (legacy definition)2'],
           inplace=True)

#for 2020 the metropolitian/not-metropolitian was a merged cell, so we need to reset index again
crime_2020['County Type'] = (crime_2020['County Type'].ffill())
crime_2020['County Type'] = crime_2020['County Type'].str.title()

#and 2008 has a weird extra column
crime_2008.drop(columns=['Unnamed: 12'], inplace=True)

# now we concatinate our list of dfs
crime_all = pd.concat(all_sheets, ignore_index=True)

#next so that crime numbers are comparable, we want to scale those by population data. 
#since we don't have numbers for 2011 and 2012 we will use 2010 data for these years. 
pop = pd.read_csv(f'/data/Pop_data.csv', encoding='latin1')
pop.head()

# will need to strip county from CTYNAME and will strinp crime just in case
pop['CTYNAME'] = pop['CTYNAME'].str.replace(r" County$", "", regex=True)

#need to rename columns for year and pivot data longer
pop.rename(columns={'POPESTIMATE2000': '2000', 'POPESTIMATE2001': '2001',
                    'POPESTIMATE2002': '2002', 'POPESTIMATE2003': '2003',
                    'POPESTIMATE2004': '2004', 'POPESTIMATE2005': '2005',
                    'POPESTIMATE2006': '2006', 'POPESTIMATE2007': '2007',
                    'POPESTIMATE2008': '2008', 'POPESTIMATE2009': '2009',
                    'POPESTIMATE2010': '2010'}, inplace=True)

#impute 2011 and 2012
pop['2011'] = pop['2010']
pop['2012'] = pop['2010']
pop = pop.drop(columns=['CENSUS2010POP', 'ESTIMATESBASE2000', 
                  'COUNTY', 'STATE', 'DIVISION', 'REGION', 'SUMLEV'])
pop_long = pd.melt(pop, ["STNAME", "CTYNAME"])

# more regex unfortunately
pop_long['variable'] = pd.to_numeric(pop_long['variable'], errors='coerce').astype('int64')
crime_all['Year'] = pd.to_numeric(crime_all['Year'], errors='coerce').astype('int64')
pop_long = pop_long.rename(columns={'value': 'Population', 'variable':'Year',
                                    'STNAME': 'State', 'CTYNAME':'County'})

pop_long['County'] = pop_long['County'].str.replace(r' Parish', '', regex=True)
pop_long['County'] = pop_long['County'].str.replace(r' city', '', regex=True)
pop_long['County'] = pop_long['County'].str.replace(r' City and Borough', '', regex=True)
pop_long['County'] = pop_long['County'].str.replace(r' Borough', '', regex=True)
pop_long['County'] = pop_long['County'].str.replace(r' Census Area', '', regex=True)
pop_long['County'] = pop_long['County'].str.replace(r' Municipality', '', regex=True)
crime_all['County'] = crime_all['County'].str.replace(r" County$", "", regex=True)
crime_all['County'] = crime_all['County'].str.replace(r' County Police Department', '', regex=True)
crime_all['County'] = crime_all['County'].str.replace(r' County Bureau of Police', '', regex=True)
crime_all['County'] = crime_all['County'].str.replace(r' Public Safety', '', regex=True)
crime_all['County'] = crime_all['County'].str.replace(r' Police Department', '', regex=True)
crime_all['County'] = crime_all['County'].str.replace(r'\s*\d+$', '', regex=True)
crime_all['County'] = crime_all['County'].str.replace(r' Unified Police Department', '', regex=True)
crime_all['County'] = crime_all['County'].str.replace(r" Sheriff's Office", '', regex=True)
crime_all['County'] = crime_all['County'].str.replace(r"\d+,", "", regex=True)
crime_all['County'] = crime_all['County'].str.replace(r" County Unified", "", regex=True)
replace_map = {'Dona Ana': 'Doña Ana', 'Du Page': 'DuPage', 'Lac Qui Parle':'Lac qui Parle',
               'La Porte': 'LaPorte', 'Lamoure': 'LaMoure'}
crime_all['County'] = crime_all['County'].replace(replace_map)

crime_all = crime_all[crime_all['Year'] <= 2012]
crime_all = crime_all[crime_all['Year'] >= 2005]

#merge into crime dataset
crime = crime_all.merge(pop_long, how='inner', 
                        on=['State', 'County', 'Year'], indicator=True)

#create crime rates 
crime['Total crime'] = crime['Violent crime'] + crime['Property crime'] 

crime_col = ['Total crime', 'Violent crime','Murder and nonnegligent manslaughter', 'Rape',
              'Robbery','Aggravated assault', 'Property crime', 'Burglary', 
              'Larceny-theft','Motor vehicle theft', 'Arson']
for c in crime_col:
    crime[f'{c}_rate'] = crime[c] / (crime['Population'] / 100000)

crime = crime.drop(columns=['County Type', '_merge'], errors='ignore')
#groupby to find averages
crime_by_county = crime.groupby(['State', 'County']).mean().reset_index()

#and write out clean dataset
output_path = f'data/derived_data/crime_by_county.csv'
crime_by_county.to_csv(output_path, index=False)

#add in county FIPS codes to crime data with a crosswalk
countyfips = pd.read_csv('data\countyfips crosswalk.csv')
countyfips = countyfips[['state_name', 'county', 'countyfips']]

#omit "County" from the end of each county name for matching
countyfips['county'] = countyfips['county'].str.replace(' County', '', regex=False)

#omit "Parish" as well so that Louisiana matches:
countyfips['county'] = countyfips['county'].str.replace(' Parish', '', regex=False)

#in crime data, rename Dona Ana, NM to have no tilde:
crime_by_county.loc[1435, 'County'] = 'Dona Ana'

crime_by_county = crime_by_county.merge(countyfips, 
                                        left_on=['State', 'County'],
                                        right_on=['state_name', 'county'],
                                        how='left',
                                        indicator=True)

assert len(crime_by_county[crime_by_county['_merge'] != 'both']) == 0

#### QCEW DATA ####

years = list(range(2005, 2013))

dataframes = {}

#read in relevant years in a loop and concatenate
for year in years:

    suffix = f'{year % 100:02d}'
    filename = os.path.join('data\QCEW Files (Raw)', f'allhlcn{suffix}.xlsx')

    if os.path.exists(filename):
        print(f'Reading in file for {year}')

        data = pd.read_excel(filename, sheet_name=0)
        dataframes[year] = data
    else:
        print(f'File not found for year {year}')
        pass

merged_df = pd.concat(dataframes.values(), ignore_index=True)

#pull out relevant variables for aggregation
subset_df = merged_df[['Area\nCode', 'Area Type', 'Ownership', 'Industry', 'Annual Average Employment', 'Annual Total Wages']]

#we want average industry concentration across our years, so sum raw numbers
grouped_df = subset_df.groupby(['Area\nCode', 'Area Type', 'Ownership', 'Industry'], as_index=False).sum()

#calculate national share for each industry
national = grouped_df[grouped_df['Area\nCode'] == 'US000']
national_total = national[national['Ownership'] == 'Total Covered']

national['Total National Employment'] = national_total.loc[63596, 'Annual Average Employment']
national['Total National Wages'] = national_total.loc[63596, 'Annual Total Wages']

national['National Employment Share'] = national['Annual Average Employment'] / national['Total National Employment']
national['National Wage Share'] = national['Annual Average Employment'] / national['Total National Employment']

#drop irrelevant columns
national = national[['Ownership', 'Industry', 'National Employment Share', 'National Wage Share']]

#compute share for counties with the same process
county = grouped_df[grouped_df['Area Type'] == 'County']
county_total = county[county['Ownership'] == 'Total Covered']

county_total = county_total.rename(columns={
    'Annual Average Employment': 'Total County Employment',
    'Annual Total Wages': 'Total County Wages'})

county_total = county_total.drop(columns=['Area Type', 'Ownership', 'Industry'])
county = county.merge(county_total, on='Area\nCode', how='left')

county['Local Employment Share'] = county['Annual Average Employment'] / county['Total County Employment']
county['Local Wage Share'] = county['Annual Total Wages'] / county['Total County Wages']

#add national concentration for each industry as a column
qcew = county.merge(national, how='left', on=['Ownership', 'Industry'])

#calculate our location quotients
qcew['Employment Location Quotient'] = qcew['Local Employment Share'] / qcew['National Employment Share']
qcew['Wage Location Quotient'] = qcew['Local Wage Share'] / qcew['National Wage Share']

#rename our county FIPS and drop irrelevant columns
qcew = qcew.rename(columns={
    'Area\nCode': 'countyfips'
}).drop(columns=[
    'Local Employment Share', 'Local Wage Share',
    'National Employment Share', 'National Wage Share'
])

#write to csv for clean dataset (but will be merged)
qcew.to_csv('data/derived_data/QCEW Data (aggregated).csv', index=False)

#### CH DATA, COUNTY SHAPEFILE ####

#read in CH data, adjust countyfips column
ch_data = pd.read_csv(r'data\chetty_hendren_causal_county_cleaned.csv', encoding='latin-1')
ch_data['County FIPS 2000'] = ch_data['County FIPS 2000'].astype('string')
ch_data['County FIPS 2000'] = ch_data['County FIPS 2000'].str.pad(width=5, side='left', fillchar='0')

#merge with qcew
ch_qcew = ch_data.merge(qcew,
                     how='left',
                     left_on='County FIPS 2000',
                     right_on='countyfips',
                     indicator=True)

print(ch_qcew[ch_qcew['_merge'] != 'both']['County Name'])

#Clifton Forge City is under 3500 people, and QCEW data does not contain information for 
#counties this small in public data for confidentiality. As it's a single county that doesn't
#match, drop.

ch_qcew = ch_qcew[ch_qcew['_merge'] == 'both']

ch_qcew = ch_qcew.drop('_merge', axis=1)

# merge with crime data. here, use an inner join - the Chetty Hendren data has more counties 
# than the FBI's crime data, although a test merge shows about 1000 non-matching counties between
# the two datasets. CH is limited by counties with enough movers, and the FBI is limited by which
# counties voluntarily report. We'll use matching counties, as we still get a large sample of 2353.

crime_by_county['countyfips'] = crime_by_county['countyfips'].astype(str)
crime_by_county = crime_by_county.drop('_merge', axis=1)

full_data = ch_qcew.merge(crime_by_county,
                     how='inner',
                     left_on='County FIPS 2000',
                     right_on='countyfips',
                     indicator=True)


#drop extraneous columns
full_data = full_data.drop(
    ['_merge', 'countyfips_y', 'State_y', 'countyfips_x', 'State_x', 'County', 'county'],
    axis=1
    )

full_data.to_csv('data\derived_data\Full Data.csv')

#read in countymap, exclude Alaska for visualization purposes
county_map = gpd.read_file(os.path.join('data\Shapefiles\County\co99_d00.shp'))
county_map = county_map[county_map['STATE'] != '02']

#counstruct countyfips
county_map['GEOID'] = (
    county_map['STATE']
    .astype(str)
    .str.pad(width=2, side='left', fillchar='0') + 
    county_map['COUNTY']
    .astype(str).str.pad(width=3, side='left', fillchar='0')
)

shape_full = county_map.merge(full_data, right_on='County FIPS 2000', left_on='GEOID', how='right')

shape_full = gpd.GeoDataFrame(shape_full, geometry='geometry')

shape_full.to_file('data\derived_data\Full Data with Geography.gpkg', driver='GPKG')