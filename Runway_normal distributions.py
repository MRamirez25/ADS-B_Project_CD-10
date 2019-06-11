import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 13)
pd.set_option('display.width', 500)



def HourCount(file):
    ####    open the file
    ADSB = pd.read_csv(file,
                       dtype={"ts": object, "icao": object, "lat": float, "lon": float, "alt": float,
                              "gs": float, "trk": float, "roc": float, "callsign": object, "fid": object,
                              "regid": object, "mdl": object, "type": object, "operator": object}, na_values = 'str')
    
    ADSB = ADSB.drop(['icao','gs','callsign','type','day','month'], axis = 1)
    
    Runway = pd.read_csv('Runway_database(v2).csv',
                         dtype={'lon_lower': float, 'lon_upper': float, 'lat_lower': float, 'lat_upper': float})
    Runway = Runway.drop(['X-B','Y-B','X-E','Y-E'], axis = 1)
    
    ### Checking if Landing or Taking off

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
    
    
    ### Counting the number of take-offs or landings, per hour, per runway, per take-off or landing
    
    Count = ADSB.groupby(['hour','runway','T/L']).size().reset_index().rename(columns={0:'count'})
    ### Making separate lists for landing and take-off
    CountL = Count[Count['T/L'] == 'Landing']
    CountT = Count[Count['T/L'] == 'Take-off']
    
    ### Count total take off and landings
    Count2 = Count.groupby(['hour']).sum().reset_index()
    
    ### Make sure all of the hours are in the index
    for q in range(24):
        if q not in Count2.hour.values:
            H = pd.DataFrame({"hour":[q]})
            Count2 = Count2.append(H, sort=True)
    
    ### Fixing total count index
    Count2 = Count2.set_index('hour')
    Count2 = Count2.reset_index().rename(columns={'count':'Total take-offs and landings'})
    Count2 = Count2.set_index('hour')
    
    ### Counting all of the planes that are landing and Counting all of the planes that are taking off
    Count2L = CountL.groupby(['hour']).sum().reset_index().rename(columns={'count':'Landing'})
    Count2T = CountT.groupby(['hour']).sum().reset_index().rename(columns={'count':'Take-off'})
    del CountL
    del CountT
    
    ### Merge two dataframes for easy bar graph making
    CountLT = pd.merge(Count2L,Count2T, how = 'left')
    
    del Count2L
    del Count2T
    
    ### Making sure all 24 hours are in the index
    for q in range(24):
        if q not in CountLT.hour.values:
            H = pd.DataFrame({"hour":[q]})
            CountLT = CountLT.append(H, sort=True)

    
    ### Fixing index
    CountLT = CountLT.set_index('hour')
    CountLT = CountLT.fillna(0)
    CountLT = CountLT.sort_index()
    
    ### Empty dataframe
    Count_runway_LT_tot = pd.DataFrame()
    

    ### Counting Landing and take-off separately for every runway (same steps as before but now in a for loop)
    for i in range(Runway.shape[0]):
        Count_runway = Count[Count.runway == Runway.loc[i,'Runway']]
        Count_runway_L = Count_runway[Count_runway['T/L'] == 'Landing']
        Count_runway_T = Count_runway[Count_runway['T/L'] == 'Take-off']
        Count_runway_L = Count_runway_L.groupby(['hour']).sum().reset_index().rename(columns={'count':'Landing'})
        Count_runway_T = Count_runway_T.groupby(['hour']).sum().reset_index().rename(columns={'count':'Take-off'})
        Count_runway_LT = pd.merge(Count_runway_L,Count_runway_T, how = 'outer')
        
        for j in range(24):
            if j not in Count_runway_LT.hour.values:
                H = pd.DataFrame({"hour":[j]})
                Count_runway_LT = Count_runway_LT.append(H, sort=True)
        
        Count_runway_LT = Count_runway_LT.set_index('hour')
        Count_runway_LT = Count_runway_LT.sort_index()
        Count_runway_LT = Count_runway_LT.rename(columns={'Landing':str(str(Runway.loc[i,'Runway'])+' Landing')}).rename(columns={'Take-off':str(str(Runway.loc[i,'Runway'])+' Take-off')})
        Count_runway_LT_tot = pd.concat([Count_runway_LT_tot,Count_runway_LT],axis = 1, sort=False)
    return Count2, CountLT, Count_runway_LT_tot


# Make empty dataframes for the variance and the mean

Counttot_var = pd.DataFrame({'Total take-offs and landings':[0]*24})
Counttot_mean = pd.DataFrame({'Total take-offs and landings':[0]*24})    #'hour':np.arange(0,24),
CountLT_mean = pd.DataFrame({'Landing':[0]*24,'Take-off':[0]*24})
CountLT_var = pd.DataFrame({'Landing':[0]*24,'Take-off':[0]*24})

### Opening Runway information dataframe

Runway = pd.read_csv('Runway_database(v2).csv',
                     dtype={'lon_lower': float, 'lon_upper': float, 'lat_lower': float, 'lat_upper': float})
Runway = Runway.drop(['X-B','Y-B','X-E','Y-E'], axis = 1)

### Making a list of runway names

Columns = []

for j in range(Runway.shape[0]):
    Columns.append(str(Runway.loc[j,'Runway'])+ ' Landing')
    Columns.append(str(Runway.loc[j,'Runway'])+ ' Take-off')

### Preparing empty DataFrame

Count_runway_LT_var = pd.DataFrame({Columns[0]:[0]*24, Columns[1]:[0]*24, Columns[2]:[0]*24, Columns[3]:[0]*24, Columns[4]:[0]*24, Columns[5]:[0]*24, Columns[6]:[0]*24, Columns[7]:[0]*24, Columns[8]:[0]*24, Columns[9]:[0]*24, Columns[10]:[0]*24, Columns[11]:[0]*24, Columns[12]:[0]*24, Columns[13]:[0]*24, Columns[14]:[0]*24, Columns[15]:[0]*24, Columns[16]:[0]*24, Columns[17]:[0]*24, Columns[18]:[0]*24, Columns[19]:[0]*24})
Count_runway_LT_mean = Count_runway_LT_var

# Setting the total amount of days to calculate

days  = 31

for i in range(1,days + 1):

    ### Opening the specific file for a certain day

    if i < 10:
        file = str('ADSB_combined/ADSB_combined_2018010'+ str(i) + '.csv')
    else:
        file = str('ADSB_combined/ADSB_combined_201801'+ str(i) + '.csv')
    print(i)
    
    ### Preparing  the DataFrames for summing

    Counttot,CountLT,Count_runway_LT_tot = HourCount(file) 
    Counttot = Counttot.fillna(0)
    CountLT = CountLT.fillna(0)
    Count_runway_LT_tot = Count_runway_LT_tot.fillna(0)
    Counttot = Counttot.sort_index()
    CountLT = CountLT.sort_index()
    
    ### Summing the amount of occurences
    
    Counttot_mean = Counttot_mean.add(Counttot)
    print('done Counttot')
    
    CountLT_mean = CountLT_mean.add(CountLT)
    print('done CountLT')
    
    Count_runway_LT_mean = Count_runway_LT_mean.add(Count_runway_LT_tot)
    #print('done Count_runway_LT_tot')
    

### Deviding total by the amount of days.

Counttot_mean = Counttot_mean.div(days)
CountLT_mean = CountLT_mean.div(days)
Count_runway_LT_mean = Count_runway_LT_mean.div(days)

### If means are already known uncomment these

#Counttot_mean = pd.read_csv('Countavgtot.csv')
#CountLT_mean = pd.read_csv('CountavgLT.csv')
#Count_runway_LT_mean = pd.read_csv('Countavg_runway_LT.csv')

#CountLT_mean = CountLT_mean.set_index('Unnamed: 0')
#Counttot_mean = Counttot_mean.set_index('Unnamed: 0')
#Count_runway_LT_mean = Count_runway_LT_mean.set_index('Unnamed: 0')

Counttot_mean.rename(columns = {'count':'Total take-offs and landings'}, inplace=True)

### Calculate variance for the 3 different statistics

for i in range(1,days + 1):
    if i < 10:
        file = str('ADSB_combined/ADSB_combined_2018010'+ str(i) + '.csv')
    else:
        file = str('ADSB_combined/ADSB_combined_201801'+ str(i) + '.csv')
    print(i)
    ### Preparing dataframes for variance calculation

    Counttot,CountLT,Count_runway_LT_tot = HourCount(file) 
    Counttot = Counttot.fillna(0)
    Counttot.rename(columns = {'count':'Total take-offs and landings'}, inplace=True)
    Counttot.sort_index(inplace=True)
    CountLT = CountLT.fillna(0)
    Count_runway_LT_tot = Count_runway_LT_tot.fillna(0)
    Counttot = Counttot.sort_index()
    CountLT = CountLT.sort_index()
    
    ### Summing the results from the calculation inside the brackets

    Counttot_var = Counttot_var.add((Counttot-Counttot_mean)**2)
    CountLT_var = CountLT_var.add((CountLT-CountLT_mean)**2)
    Count_runway_LT_var = Count_runway_LT_var.add((Count_runway_LT_tot-Count_runway_LT_mean)**2)

### Finishing variance calculation by deviding the sum by (days-1)

Counttot_var = 1/(days-1)*Counttot_var
CountLT_var = 1/(days-1)*CountLT_var
Count_runway_LT_var = 1/(days-1)*Count_runway_LT_var


### Saving the mean
Counttot_mean.to_csv('New/Counttot_mean.csv')
CountLT_mean.to_csv('New/CountLT_mean.csv')
Count_runway_LT_mean.to_csv('New/Count_runway_LT_mean.csv')

### Saving the Variance
Counttot_var.to_csv('New/Counttot_var.csv')
CountLT_var.to_csv('New/CountLT_var.csv')
Count_runway_LT_var.to_csv('New/Count_runway_LT_var.csv')
