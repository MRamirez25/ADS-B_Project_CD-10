import pandas as pd

pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 500)

#### input: pandas dataframe of your ADS-B data
#### output: pandas dataframe of all detected landings and take-offs for the specified runways
def ADSB_Runway(ADSB):
    ####    Drop undesired columns
    ADSB = ADSB.drop(['icao','gs','callsign','type','hour','month','year'], axis = 1)

    ####    Read and drop from Runway database
    Runway = pd.read_csv('Runway_database(v2).csv',
                         dtype={'lon_lower': float, 'lon_upper': float, 'lat_lower': float, 'lat_upper': float})
    Runway = Runway.drop(['X-B','Y-B','X-E','Y-E'], axis = 1)

    ####    Only keep aircraft below 5000ft and above 0
    ADSB = ADSB[(ADSB['alt']<5000) & (ADSB['alt']>0)]

    ####    Allocate runway to flight/aircraft
    ####    First set heading margin to +/- 5 for all runways
    ####    For Eindhoven, Maastricht & Groningen set margin to +/- 50 | For Polderbaan set margin to +/- 10
    for i in range(Runway.shape[0]):
        if i == 6 or i ==7 or i == 9:
            e = 50.
        elif i ==2:
            e = 10
        else:
            e = 5.
    ####    Locate and add runway to dataframe
        ADSB.loc[((ADSB['lon']>Runway.loc[i,'lon_lower']) & (ADSB['lon']<Runway.loc[i,'lon_upper']) & (ADSB['lat']>Runway.loc[i,'lat_lower']) &
                 (ADSB['lat']<Runway.loc[i,'lat_upper']) & ((ADSB['trk'] > Runway.loc[i,'Track 1'] - e) &
                (ADSB['trk'] < Runway.loc[i,'Track 1'] + e) | (ADSB['trk'] > Runway.loc[i,'Track 2'] - e) & (ADSB['trk'] < Runway.loc[i,'Track 2'] + e))
                 ), 'runway'] = Runway.loc[i,'Runway']

    ####   Drop 'nan' runways
    ADSB = ADSB[pd.notnull(ADSB['runway'])]

    ####    For positive ROC add 'Take-off', for negative ROC add 'Landing'
    ADSB.loc[(ADSB['roc']>0.), 'T/L'] = 'Take-off'
    ADSB.loc[(ADSB['roc']<0.), 'T/L'] = 'Landing'

    ####    Drop duplicate flight ID's
    ####    Only keep first data point for departing aircraft
    ADSB.loc[ADSB['T/L'] == 'Take-off'] = (ADSB.loc[ADSB['T/L'] == 'Take-off']).drop_duplicates(['fid'], keep='first')

    ####    Only keep last data point for arriving aircraft
    ADSB.loc[ADSB['T/L'] == 'Landing'] = (ADSB.loc[ADSB['T/L'] == 'Landing']).drop_duplicates(['fid'], keep='last')

    ####    For non Rotterdam flights, check proper ROC and drop duplicates if necessary
    ADSB.loc[ADSB['runway'] != 'Rotterdam'] = ADSB.loc[ADSB['runway'] != 'Rotterdam'][(ADSB.loc[ADSB['runway'] != 'Rotterdam']['roc']> 500.) | (ADSB.loc[ADSB['runway'] != 'Rotterdam']['roc'] < -150.)]
    ADSB = ADSB[pd.notnull(ADSB['runway'])]
    ADSB = ADSB[pd.notnull(ADSB['T/L'])]
    ADSB.set_index(['ts'], inplace = True)

    return(ADSB)
    

####    Open the original ADS-B files and write to new file
for i in range(1,32):
    if i<10:
        ADSB = pd.read_csv(str('ADSB_combined/ADSB_combined_2018010'+ str(i) + '.csv'),
                       dtype={"ts": object, "icao": object, "lat": float, "lon": float, "alt": float,
                              "gs": float, "trk": float, "roc": float, "callsign": object, "fid": object,
                              "regid": object, "mdl": object, "type": object, "operator": object}, na_values = 'str')
        ADSB = ADSB_Runway(ADSB)
        ADSB.to_csv(str('ADSB_Runway_Det/ADSB_Runway_Det_2018010'+ str(i) +'.csv'))
        print(i)

    else:
        ADSB = pd.read_csv((str('ADSB_combined/ADSB_combined_201801'+ str(i) + '.csv')),
                   dtype={"ts": object, "icao": object, "lat": float, "lon": float, "alt": float,
                          "gs": float, "trk": float, "roc": float, "callsign": object, "fid": object,
                          "regid": object, "mdl": object, "type": object, "operator": object}, na_values = 'str')
        ADSB = ADSB_Runway(ADSB)
        ADSB.to_csv(str('ADSB_Runway_Det/ADSB_Runway_Det_201801'+ str(i) +'.csv'))
        print(i)
