import pandas as pd
import matplotlib.pyplot as plt

CountLT = pd.read_csv('CountavgLT.csv')
Counttot = pd.read_csv('Countavgtot.csv')
Countrunway = pd.read_csv('Countavg_runway_LT.csv')
Meancount = pd.read_csv('Mean_Count_Runway_January.csv')
Daycount = pd.read_csv('Total_RunwayCount_per_dag_January.csv')

Runway = pd.read_csv('Runway_database(v2).csv',
                         dtype={'lon_lower': float, 'lon_upper': float, 'lat_lower': float, 'lat_upper': float})
Runway = Runway.drop(['X-B','Y-B','X-E','Y-E','lon_lower','lon_upper','lat_lower','lat_upper','Track 1','Track 2'], axis = 1)


CountLT = CountLT.set_index('Unnamed: 0')
Counttot = Counttot.set_index('Unnamed: 0')
Countrunway = Countrunway.set_index('Unnamed: 0')
Daycount = Daycount.set_index('Unnamed: 0')
Meancount = Meancount.set_index('Unnamed: 0')

Counttot.rename(columns = {'count':'Total take-offs and landings'}, inplace=True)
BarCountLT = CountLT.plot.bar()
BarCountLT = BarCountLT.set_xlabel('Hour')
plt.ylabel('Number of movements')
BarCountLT = BarCountLT.get_figure()
BarCountLT.tight_layout()
BarCountLT.savefig('Figures/BarCountLT.pdf',format='pdf')

BarCounttot = Counttot.plot.bar()
BarCounttot = BarCounttot.set_xlabel('Hour')
plt.ylabel('Number of movements')
BarCounttot = BarCounttot.get_figure()
BarCounttot.tight_layout()
BarCounttot.savefig('Figures/BarCounttot.pdf',format='pdf')

BarMeancount = Meancount.plot.bar()
BarMeancount = BarMeancount.set_xlabel('Runway')
BarMeancount = BarMeancount.get_figure()
BarMeancount.tight_layout()
BarMeancount.savefig('Figures/BarMeancount.pdf',format='pdf')



for i in range(Runway.shape[0]):
    if Runway.loc[i,'Runway'] in Daycount:
        BarDaycount = Daycount.plot.bar(y=Runway.loc[i,'Runway'],color = 'C0')
        BarDaycount = BarDaycount.set_xlabel('Day of the month')
        BarDaycount = BarDaycount.get_figure()
        BarDaycount.tight_layout()
        BarDaycount.savefig(str('Figures/BarDaycount_'+Runway.loc[i,'Runway']+'.pdf'),format='pdf')

for i in range(int(len(Countrunway.columns)/2)):
    j = i * 2
    BarRunway = Countrunway[[list(Countrunway)[j],list(Countrunway)[j+1]]].plot.bar()
    BarRunway = BarRunway.set_xlabel('Hour')
    plt.ylabel('Number of movements')
    BarRunway = BarRunway.get_figure()
    BarRunway.tight_layout()
    BarRunway.savefig(str('Figures/BarRunway_'+list(Countrunway)[j]+'_and_Take-off.pdf').replace(" ","_"),format='pdf')
