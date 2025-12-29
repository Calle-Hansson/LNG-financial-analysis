# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 11:44:23 2025

@author: calle

Imports AIS data that is locally saved but originally from the NOAA accesais program.
The data is from the 04-01-2024 to 31-12-2024

"""


import pandas as pd

df1 = pd.read_csv("AIS_176632433230372488_844-1766324332611.csv")
df2 = pd.read_csv("AIS_176632433230372488_1544-1766351527715.csv")
df= pd.concat([df1,df2], axis=0)



#%%
'''The data is cleaned'''
cols_to_keep=[
    'MMSI','BaseDateTime',
    'LAT', 'LON', 'SOG', 'COG', 'Heading',
    'VesselType', 'Status', 'Length',
    'Width', 'Draft', 'Cargo'
    ]

df = df[cols_to_keep]
          

'''The program filters out any possible LNG Tankers and discards the rest of the datapoints'''
df= df[
       (df['VesselType'].between(80,89)) &
       (
        (df['Cargo']==84) | 
        ((df['Length'] > 250) & df['Draft'] > 10)
        ) & df['Heading'].between(0,180)
       ]



df = df.reset_index(drop= True)

'''The data is sorted'''
df=df.sort_values(['MMSI','BaseDateTime'])
    
#%%


'''The program creates the "leaves port event" by geocashing the area inside the port and the area just outside.
If 1 that was previosly in port, exits the port: that will be registered as an export event and added to a new df'''


df['in_port'] = (
    df['LAT'].between(29.691019595359222,29.74943387941589) &
    df['LON'].between(-93.91080390566599,-93.820682878836 )
    
    )
    
df['out_of_port'] = (
    df['LAT'].between(29.591137142289384, 29.6888969407879) &
    df['LON'].between(-93.8583564209909, -93.77053659974136)
    
    )



prev_in_port= df.groupby('MMSI')['in_port'].shift(1)
df['Leave_event'] = (
    (prev_in_port == True) &
    (df['in_port'] == False)    
    
    )

df['BaseDateTime'] = pd.to_datetime(df['BaseDateTime'], errors= 'coerce')
departures = df[df['Leave_event']].copy()
departures['Date'] = departures['BaseDateTime'].dt.date
ships_per_day= departures.groupby('Date')['MMSI'].nunique()

ships_per_day.index = pd.to_datetime(ships_per_day.index)

full_index = pd.date_range(ships_per_day.index.min(), ships_per_day.index.max(), freq = "D")
ships_per_day_full = ships_per_day.reindex(full_index, fill_value=0)

ships_per_day_full.index.name = "Date"
ships_per_day_full.name = "Exports"
print(ships_per_day_full)


ships_per_day_full.to_csv('LNG_Exports.csv', index= True, header=False)
print("LNG Exports saved")

'''LNG_Exports.csv contains a df of every day in the data set and the amount of recorded exports for each day'''
















