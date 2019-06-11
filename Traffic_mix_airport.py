import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

####    Read and drop from Runway database
Runway = pd.read_csv('Runway_database(v2).csv',
                     dtype={'lon_lower': float, 'lon_upper': float, 'lat_lower': float, 'lat_upper': float})
Runway = Runway.drop(['X-B','Y-B','X-E','Y-E'], axis = 1)

####    Make new dataframe
ADSB = pd.DataFrame()

####    Read Runway Determination file and add to the dataframe
for i in range(1,32):
    if i <10:
        ADSBi = pd.read_csv(str('ADSB_Runway_Det/ADSB_Runway_Det_2018010' + str(i) + '.csv'), dtype={"ts": object, "lat": float, "lon": float, "alt": float,
                             "trk": float, "roc": float, "fid": object, "regid": object, "mdl": object, "operator": object, "runway": object, "T/L": object})
        ADSB = pd.DataFrame.append(ADSB, ADSBi)        

    else:
        ADSBi = pd.read_csv(str('ADSB_Runway_Det/ADSB_Runway_Det_201801' + str(i) + '.csv'), dtype={"ts": object, "lat": float, "lon": float, "alt": float,
                             "trk": float, "roc": float, "fid": object, "regid": object, "mdl": object, "operator": object, "runway": object, "T/L": object})
        ADSB = pd.DataFrame.append(ADSB, ADSBi)        



####    Make pie chart for models per runway
for i in range(Runway.shape[0]):            

    ####    Only pick one runway
    ADSB_Runway = ADSB[ADSB['runway'] == Runway.loc[i,'Runway']]

    ####    Find all unique models in dataframe
    Model = ADSB_Runway.mdl.unique()

    ####    Produce percentages
    Count = np.zeros(len(Model))
    ValueCount = ADSB_Runway.groupby(['mdl']).size().reset_index().rename(columns={0:'count'})
    SumCount = sum(ValueCount['count'])
    ValueCount['count'] = ValueCount['count']/SumCount *100
    print(Runway.loc[i,'Runway'],ValueCount)

    ####    Make 'other' as sum of all types % < 1.5
    PercCount = sum(ValueCount['count'])
    ValueCount = ValueCount[ValueCount['count'] > 1.5]
    PercCount2 = sum(ValueCount['count'])
    Other = (PercCount - PercCount2)

    ####    Only show non-zero %
    Count = np.array(ValueCount['count'])
    Model = np.array(ValueCount['mdl'])
    Count = np.append(Count, [Other])
    Model = np.append(Model, ['Other'])
    Model = Model[Count > 0]
    Count = Count[Count > 0]
    Colors = cm.gist_rainbow(np.arange(len(Count))/len(Count))

    ####    Plot pie chart     
    plt.pie(Count, labels=Model, autopct='%1.1f%%', pctdistance=0.9, rotatelabels=True, colors=Colors, startangle=90, wedgeprops={"edgecolor":"w",'linewidth': 1}, textprops={'size': 'x-large'})
    plt.title(str('Traffic mix ' + Runway.iloc[i]['Runway']), fontsize = 20, y=1.08)
    plt.show()

####    Overall pie chart (model)

ADSB_schiphol = ADSB.loc[(ADSB['runway'] != 'Eindhoven') & (ADSB['runway'] != 'Rotterdam') & (ADSB['runway'] != 'Maastricht') & (ADSB['runway'] != 'Groningen')] 

####    Find all unique models in dataframe
Model = ADSB_schiphol.mdl.unique()

####    Produce percentages
Count = np.zeros(len(Model))
ValueCount = ADSB_schiphol.groupby(['mdl']).size().reset_index().rename(columns={0:'count'})
SumCount = sum(ValueCount['count'])
ValueCount['count'] = ValueCount['count']/SumCount *100
print(ValueCount)

#### Make 'other' as sum of all types % < 1.5
PercCount = sum(ValueCount['count'])
ValueCount = ValueCount[ValueCount['count'] > 1.0]
PercCount2 = sum(ValueCount['count'])
Other = (PercCount - PercCount2)
Count = np.array(ValueCount['count'])
Model = np.array(ValueCount['mdl'])

####    Only show non-zero %
Count = np.append(Count, [Other])
Model = np.append(Model, ['Other'])
Model = Model[Count > 0]
Count = Count[Count > 0]
Colors = cm.gist_rainbow(np.arange(len(Count))/len(Count))

####    Plot pie chart
plt.pie(Count, labels=Model, autopct='%1.1f%%', pctdistance=0.9, rotatelabels=True, colors=Colors, startangle=90, wedgeprops={"edgecolor": "w",'linewidth': 1}, textprops={'size': 'x-large'})
plt.title('Overall traffic mix Schiphol', fontsize = 20, y=1.08)
plt.show()

######    Overall pie chart (airline)
##Model = ADSB_schiphol.operator.unique()
##Count = np.zeros(len(Model))
##ValueCount = ADSB_schiphol.groupby(['operator']).size().reset_index().rename(columns={0:'count'})
##SumCount = sum(ValueCount['count'])
##ValueCount['count'] = ValueCount['count']/SumCount *100
##PercCount = sum(ValueCount['count'])
##ValueCount = ValueCount[ValueCount['count'] > 1.0]
##PercCount2 = sum(ValueCount['count'])
##Other = (PercCount - PercCount2)
##Count = np.array(ValueCount['count'])
##Model = np.array(ValueCount['operator'])
##Count = np.append(Count, [Other])
##Model = np.append(Model, ['Other'])
##Model = Model[Count > 0]
##Count = Count[Count > 0]
##Colors = cm.gist_rainbow(np.arange(len(Count))/len(Count))
##
##plt.pie(Count, labels=Model, autopct='%1.1f%%', pctdistance=0.95, rotatelabels=True, colors=Colors, startangle=90, wedgeprops={"edgecolor":"w",'linewidth': 1}, textprops={'size': 'large'})
##plt.title('Overall airlines Schiphol', fontsize = 20, y=1.08)
##plt.show()
