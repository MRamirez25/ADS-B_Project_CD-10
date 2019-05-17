import pandas as pd

pd.set_option('display.max_columns', 13)
pd.set_option('display.width', 500)

Aircraft = pd.read_csv('aircraft_db.csv', dtype={"icao": object, "regid": object, "mdl": object, "type": object, "operator": object})
Aircraft['icao']= Aircraft['icao'].apply(lambda x: x.upper())
print('done with Aircraft database')


def Combine(file, Aircraft):
    ADSB            = pd.read_csv(str('adsb_decoded/'+file), dtype={"ts": float, "icao": object, "lat": float, "lon": float, "alt": float,
                                               "gs": float, "trk": float, "roc": float, "callsign": object, "fid": object})
    Combined        = pd.merge(ADSB,Aircraft, how='left')
    Combined['ts'] = pd.to_datetime(Combined['ts'], unit = 's', utc = True)
    Combined['ts'] = Combined['ts'].dt.tz_convert('Europe/Amsterdam')
    Combined['hour'] = Combined['ts'].dt.hour
    Combined['day'] = Combined['ts'].dt.day
    Combined['month'] = Combined['ts'].dt.month
    Combined['year'] = Combined['ts'].dt.year
    Combined.set_index(['ts'], inplace = True)
    Combined = Combined.sort_index()
    return Combined

for i in range(8,32):
    if i<10:
        print(i)
        file = str('ADSB_DECODED_2018010'+ str(i) + '.csv')
        print(file)
        Combined = Combine(file,Aircraft)
        print('Done combining ' + str(i))
        Combined.to_csv(str('ADSB_combined/ADSB_combined_2018010'+ str(i) +'.csv'))
        print('Done printing ' + str(i))
    else:
        print(i)
        file = str('ADSB_DECODED_201801'+ str(i) + '.csv')
        print(file)
        Combined = Combine(file,Aircraft)
        print('Done combining ' + str(i))
        Combined.to_csv(str('ADSB_combined/ADSB_combined_201801'+ str(i) +'.csv'))
        print('Done printing ' + str(i))
        
    


    
    
