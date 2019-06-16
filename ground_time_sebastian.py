import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statistics as st
g_time=pd.DataFrame()
result=pd.DataFrame()
## from day 1 to day 9
for i in range(1,10):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    gtime = pd.read_csv('ADSB_Runway_Det_2018010'+ str(i)+'.csv',
                       dtype={"ts": object,"lat": float, "lon": float, "alt": float,
                               "trk": float, "roc": float, "fid": object,
                              "regid": object, "mdl": object,"day":float,"runway":object,"T/L":object,
                              "operator": object}, na_values = 'str')
    gtime = gtime.drop(['lat','lon','alt','trk','roc','operator','day',],axis = 1)
    #time stamp correction 
    time=pd.to_datetime(gtime['ts'])
    ghour=time.dt.hour
    gminute=time.dt.minute
    gminute=gminute.div(60)
    ghour=ghour+gminute
    gtime=gtime.drop(['ts'], axis=1)
    ghour=ghour.to_frame()
    gtime=ghour.join(gtime)
    gtime=gtime.drop(gtime.columns[1], axis=1)
        # Find the grounf time and filter data to specific model
    lst=gtime.regid.unique().tolist()
    lst1=['b737','b777','b787','b747','b767','a318','a319','a320','a350','a380','e751'
          ,'rj85','bcs3','e195','lj75']
    g_time=pd.DataFrame()
    for i in range(len(lst)):
        e=gtime.loc[gtime['regid'].isin([lst[i]])]
        if e['T/L'].iloc[0]=='Landing':
            e.drop(e.index[0])
            z=e['ts'].diff().iloc[1::2].to_frame()
            g_time=g_time.append(z,ignore_index=False)
        else:
            z=e['ts'].diff().iloc[::2].to_frame()
            g_time=g_time.append(z,ignore_index=False)
            
    test = gtime.drop(['ts','regid'], axis=1)
    result1 = test.join(g_time, how='inner').dropna()
    result1.columns= ['mdl','runway','TL','ts',] 
    result1=result1[result1.TL != 'Landing']
    result=result.append(result1,ignore_index=False,)
#############################################################################################
    # open the files for the last 20 days of the month
#############################################################################################
for i in range(10,32):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    gtime = pd.read_csv('ADSB_Runway_Det_201801'+ str(i)+'.csv',
                       dtype={"ts": object,"lat": float, "lon": float, "alt": float,
                               "trk": float, "roc": float, "fid": object,
                              "regid": object, "mdl": object,"day":float,"runway":object,"T/L":object,
                              "operator": object}, na_values = 'str')
    gtime = gtime.drop(['lat','lon','alt','trk','roc','operator','day',],axis = 1)
    #time stamp correction 
    time=pd.to_datetime(gtime['ts'])
    ghour=time.dt.hour
    gminute=time.dt.minute
    gminute=gminute.div(60)
    ghour=ghour+gminute
    gtime=gtime.drop(['ts'], axis=1)
    ghour=ghour.to_frame()
    gtime=ghour.join(gtime)
    gtime=gtime.drop(gtime.columns[1], axis=1)
        # Find the grounf time and filter data to specific model
    lst=gtime.regid.unique().tolist()
    lst1=['b737','b777','b787','b747','b767','a318','a319','a320','a350','a380','e751'
          ,'rj85','bcs3','e195','lj75']
    g_time=pd.DataFrame()
    for i in range(len(lst)):
        e=gtime.loc[gtime['regid'].isin([lst[i]])]
        if e['T/L'].iloc[0]=='Landing':
            e.drop(e.index[0])
            z=e['ts'].diff().iloc[1::2].to_frame()
            g_time=g_time.append(z,ignore_index=False)
        else:
            z=e['ts'].diff().iloc[::2].to_frame()
            g_time=g_time.append(z,ignore_index=False)
            
    test = gtime.drop(['ts','regid'], axis=1)
    result1 = test.join(g_time, how='inner').dropna()
    result1.columns= ['mdl','runway','TL','ts',] 
    result1=result1[result1.TL != 'Landing']
    result=result.append(result1,ignore_index=False,)
# Make individual data for each model    
b737=result[(result['mdl'].isin(['b738','b739','b737','b733']))]
b777=result[(result['mdl'].isin(['b77l','b77w','b772']))]
b787=result[(result['mdl'].isin(['b788','b789']))]
b747=result[(result['mdl'].isin(['b744','b748']))]
b767=result[(result['mdl'].isin(['b763','b763',]))]
a318=result[(result['mdl'].isin(['a318']))]
a319=result[(result['mdl'].isin(['a319']))]
a320=result[(result['mdl'].isin(['a320']))]
a321=result[(result['mdl'].isin(['a321']))]
a330=result[(result['mdl'].isin(['a332','a333']))]
a350=result[(result['mdl'].isin(['a359']))]
a380=result[(result['mdl'].isin(['a388']))]
e751=result[(result['mdl'].isin(['e751']))]
e190=result[(result['mdl'].isin(['e190']))]
rj85=result[(result['mdl'].isin(['rj85']))]
bcs3=result[(result['mdl'].isin(['bcs3']))]
e195=result[(result['mdl'].isin(['e195']))]
lj75=result[(result['mdl'].isin(['lj75']))]

# Plot results of overall data
ser=b737['ts'].values.tolist()
result.hist(column=None, by=None, grid=True, xlabelsize=None, xrot=None, ylabelsize=None,
            yrot=None, ax=None, sharex=False,sharey=False, figsize=None,density=True,
            layout=None,bins=50)
xt = plt.xticks()[0]  
xmin, xmax = min(xt), max(xt)  
lnspc = np.linspace(xmin, xmax, len(ser))
#### gamma distribution
##ag,bg,cg = stats.gamma.fit(ser)  
##pdf_gamma = stats.gamma.pdf(lnspc, ag, bg,cg)  
##plt.plot(lnspc, pdf_gamma, label="Gamma")

###normal distribution
##(mu, sigma) = stats.norm.fit(ser)
##ndist = stats.norm.pdf(np.arange(24), mu, sigma)
##l1 = plt.plot(np.arange(24), ndist, 'r--', linewidth=2)
##
##
###beta distribution
##p1, p2, p3, p4 = stats.beta.fit(ser)
##bdist = stats.beta.pdf(np.arange(24), p1, p2, p3, p4)
##l3 = plt.plot(np.arange(24), bdist, 'g--', linewidth=2)


#kde distribution
xs = np.arange(0, 24, 0.1)
density = stats.gaussian_kde(ser)
l4 = plt.plot(xs, density(xs), 'y--', linewidth=2)

#############################################################################
print('Individual statistics of the following models are available:')
print(lst1)
plt.title('Boeing-737 histogram')
plt.xlabel('Time[hours]')
plt.ylabel('Probability density')
plt.show()

