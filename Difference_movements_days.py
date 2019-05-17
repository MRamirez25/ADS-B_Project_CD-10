# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 08:58:39 2019

@author: Frank
"""

import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 13)
pd.set_option('display.width', 500)


def RunwayCount(file):
    ####    open the file
    ADSB = pd.read_csv(file,
                       dtype={"ts": object, "icao": object, "lat": float, "lon": float, "alt": float,
                              "gs": float, "trk": float, "roc": float, "callsign": object, "fid": object,
                              "regid": object, "mdl": object, "type": object, "operator": object}, na_values = 'str')
    
    ADSB = ADSB.drop(['icao','gs','callsign','type'], axis = 1)
    
    Runway = pd.read_csv('Runway_database(v2).csv',
                         dtype={'lon_lower': float, 'lon_upper': float, 'lat_lower': float, 'lat_upper': float})
    Runway = Runway.drop(['X-B','Y-B','X-E','Y-E'], axis = 1)
    
    ADSB = ADSB[(ADSB['alt']<5000) & (ADSB['alt']>0)]
    ADSB = ADSB[ADSB.year == 2018]
    
    for i in range(Runway.shape[0]):
        if i == 6 or i ==7 or i == 9:
            e = 50.
        else:
            e = 5.
        ADSB.loc[((ADSB['lon']>Runway.loc[i,'lon_lower']) &
                 (ADSB['lon']<Runway.loc[i,'lon_upper']) &
                 (ADSB['lat']>Runway.loc[i,'lat_lower']) &
                 (ADSB['lat']<Runway.loc[i,'lat_upper']) &
                 ((ADSB['trk'] > Runway.loc[i,'Track 1'] - e) &
                  (ADSB['trk'] < Runway.loc[i,'Track 1'] + e) |
                  (ADSB['trk'] > Runway.loc[i,'Track 2'] - e) &
                  (ADSB['trk'] < Runway.loc[i,'Track 2'] + e))
                 ), 'runway'] = Runway.loc[i,'Runway']
    
    ADSB = ADSB[pd.notnull(ADSB['runway'])]
    ADSB.loc[(ADSB['roc']>0.), 'T/L'] = 'Take-off'
    ADSB.loc[(ADSB['roc']<0.), 'T/L'] = 'Landing'
    ADSB.loc[ADSB['T/L'] == 'Take-off'] = (ADSB.loc[ADSB['T/L'] == 'Take-off']).drop_duplicates(['fid'], keep='first')
    ADSB.loc[ADSB['T/L'] == 'Landing'] = (ADSB.loc[ADSB['T/L'] == 'Landing']).drop_duplicates(['fid'], keep='last')
    
    ADSB.loc[ADSB['runway'] != 'Rotterdam'] = ADSB.loc[ADSB['runway'] != 'Rotterdam'][(ADSB.loc[ADSB['runway'] != 'Rotterdam']['roc']> 500.) | (ADSB.loc[ADSB['runway'] != 'Rotterdam']['roc'] < -200.)]
    ADSB = ADSB[pd.notnull(ADSB['runway'])]
    ADSB = ADSB[pd.notnull(ADSB['T/L'])]
    ADSB = ADSB.drop_duplicates(['fid'], keep='last')
    
    df = ADSB.drop(['lat','lon','alt','trk','roc','regid','mdl','operator','hour','year'], axis = 1)
    Count = df['runway'].value_counts()
    return Count

Counttot = pd.DataFrame()

for i in range(1,32):
    if i < 10:
        file = str('ADSB_combined/ADSB_combined_2018010'+ str(i) + '.csv')
    else:
        file = str('ADSB_combined/ADSB_combined_201801'+ str(i) + '.csv')
    print(i)
    
    Count = RunwayCount(file)
    Counttot = pd.DataFrame.append(Counttot,Count)
    
Countmean = Counttot.mean()
Countmean = Countmean.to_frame()
Countmean.columns = ['Average number of flights']
Counttot = Counttot.set_index(np.arange(1,Counttot.shape[0]+1))

Countvar = Counttot.var()
Countvar = Countvar.to_frame()
Countvar.columns = ['Variance of flights']

Countvar.to_csv('Variance_Count_Runway_January.csv')
Countmean.to_csv('Mean_Count_Runway_January.csv')
Counttot.to_csv('Total_RunwayCount_per_day_January.csv')


