# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 17:49:45 2017

@author: CStorm
"""
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

UniversityTowns_raw = pd.read_table(filepath_or_buffer = 'F:\GITHub\Coursera\Intro to Data Science in Python\IntroToDataScienceInPython/university_towns.txt', header=None)
UniversityTowns_raw.rename(columns={0:'Area'}, inplace=True)

#stateIndices=UniversityTowns_raw[UniversityTowns_raw['Area'].str.contains('edit')].index
#stateIndicesList=stateIndices.tolist()

stateList = []
cityList = []
for region in UniversityTowns_raw.Area:
    if 'edit' in region:
        currentState = region   
    else:
        cityList.append(region)
        stateList.append(currentState)

UniversityTowns = pd.DataFrame(data={'State':stateList, 'RegionName':cityList})
UniversityTowns.State = UniversityTowns.State.apply(lambda state: state.rstrip('edit]').rstrip('['))
UniversityTowns.RegionName = UniversityTowns.RegionName.apply(lambda region: region.split('(')[0])
UniversityTowns.RegionName = UniversityTowns.RegionName.apply(lambda region: region.rstrip(' '))
    

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    UniversityTowns_raw = pd.read_table(filepath_or_buffer = "university_towns.txt", header=None)
    UniversityTowns_raw.rename(columns={0:'Area'}, inplace=True)

    stateList = []
    cityList = []
    for region in UniversityTowns_raw.Area:
        if 'edit' in region:
            currentState = region        
        else:
            cityList.append(region)
            stateList.append(currentState)

    UniversityTowns = pd.DataFrame(data={'State':stateList, 'RegionName':cityList})
    UniversityTowns.State = UniversityTowns.State.apply(lambda state: state.rstrip('edit]').rstrip('['))
    UniversityTowns.RegionName = UniversityTowns.RegionName.apply(lambda region: region.split('(')[0])
    UniversityTowns.RegionName = UniversityTowns.RegionName.apply(lambda region: region.rstrip(' '))

    UniversityTowns = UniversityTowns[['State', 'RegionName']]
    
    return UniversityTowns
get_list_of_university_towns()




GDP_raw = pd.read_excel('gdplev.xls')
GDP = GDP_raw[['Unnamed: 4','Unnamed: 6']][219:]
GDP.rename(columns={'Unnamed: 4':'Quarter', 'Unnamed: 6':'GDP'}, inplace=True)

GDP['Change']=GDP.GDP-GDP.GDP.shift(1)
GDP['Next_Change']=GDP.Change.shift(-1)
GDP[(GDP.Change<0) & (GDP.Next_Change<0)]
GDP['Recession']=False
GDP.set_value(GDP[(GDP.Change<0) & (GDP.Next_Change<0)].index.tolist(), 'Recession', True)


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    GDP_raw = pd.read_excel('gdplev.xls')
    GDP = GDP_raw[['Unnamed: 4','Unnamed: 6']][219:]
    GDP.rename(columns={'Unnamed: 4':'Quarter', 'Unnamed: 6':'GDP'}, inplace=True)

    GDP['Change']=GDP.GDP-GDP.GDP.shift(1)
    GDP['Next_Change']=GDP.Change.shift(-1)
    GDP[(GDP.Change<0) & (GDP.Next_Change<0)]
    GDP['Recession']=False
    GDP.set_value(GDP[(GDP.Change<0) & (GDP.Next_Change<0)].index.tolist(), 'Recession', True)
    
    recession_start = GDP.Quarter[(GDP.Change<0) & (GDP.Next_Change<0)].iloc[0]
    
    return recession_start
get_recession_start()

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    GDP_raw = pd.read_excel('gdplev.xls')
    GDP = GDP_raw[['Unnamed: 4','Unnamed: 6']][219:]
    GDP.rename(columns={'Unnamed: 4':'Quarter', 'Unnamed: 6':'GDP'}, inplace=True)

    GDP['Change']=GDP.GDP-GDP.GDP.shift(1)
    GDP['Previous_Change']=GDP.Change.shift(1)
    GDP['Next_Change']=GDP.Change.shift(-1)

    GDP['Recession']=False
    GDP.set_value(GDP[(GDP.Change<0) & ((GDP.Next_Change<0)|(GDP.Previous_Change<0))].index.tolist(), 'Recession', True)
               
    last_recession_month = GDP[GDP['Recession']==True].iloc[-1].Quarter
    recession_end = GDP.loc[GDP[GDP['Quarter']==last_recession_month].index.tolist()[0]+2].Quarter 
        
    return recession_end
get_recession_end()

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    GDP_raw = pd.read_excel('gdplev.xls')
    GDP = GDP_raw[['Unnamed: 4','Unnamed: 6']][219:]
    GDP.rename(columns={'Unnamed: 4':'Quarter', 'Unnamed: 6':'GDP'}, inplace=True)

    GDP['Change']=GDP.GDP-GDP.GDP.shift(1)
    GDP['Previous_Change']=GDP.Change.shift(1)
    GDP['Next_Change']=GDP.Change.shift(-1)

    GDP['Recession']=False
    GDP.set_value(GDP[(GDP.Change<0) & ((GDP.Next_Change<0)|(GDP.Previous_Change<0))].index.tolist(), 'Recession', True) 
                
    recession_bottom = GDP[GDP['Recession']==True].sort_values('GDP').iloc[0].Quarter
    
    return recession_bottom
get_recession_bottom()


Housing_raw = pd.read_csv('City_Zhvi_AllHomes.csv')
Housing = Housing_raw.drop(Housing_raw.columns[6:51], axis = 1)

Housing = Housing.set_index(['State', 'RegionName'])

#Housing.groupby(pd.PeriodIndex(Housing.columns, freq='Q'), axis=1).mean()

HousingPriceMonthly = Housing[Housing.columns[4:205]]
HousingPriceQuarterly=HousingPriceMonthly.groupby(pd.PeriodIndex(HousingPriceMonthly.columns, freq='Q'), axis=1).mean()

StringColumns = HousingPriceQuarterly.columns.to_series().astype(str).reset_index().drop(0, axis=1)
    
StringColumns = HousingPriceQuarterly.columns.format()
HousingPriceQuarterly.columns = [x.lower() for x in StringColumns]
    






