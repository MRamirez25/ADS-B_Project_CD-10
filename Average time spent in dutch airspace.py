import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
pd.set_option('display.max_columns', 13)
pd.set_option('display.width', 500)


def main_data (file,no):
    ####    open the files and give type of column data
    Main_Data = pd.read_csv(file,
                            dtype={"ts": object, "icao": object, "lat": float, "lon": float, "alt": float,
                                   "gs": float, "trk": float, "roc": float, "callsign": object, "fid": object,
                                   "regid": object, "mdl": object, "type": object, "operator": object})
    print('Done with Data')
    #requried Parameters
    Main_Data=Main_Data[['lat','lon',"alt", "fid",'ts','roc']]


    #Boundary constraint area 
    Main_Data = Main_Data[(Main_Data["lat"] >= 50.50) & (Main_Data["lat"] <= (53.5)) & (Main_Data["lon"] >= 3.5) & (Main_Data["lon"] <= (7))]

    #Extracting dat time munite and second from timestamp
    Main_Data['ts'] = pd.to_datetime(Main_Data['ts'], utc = True)
    Main_Data['ts'] =Main_Data['ts'].dt.tz_convert('Europe/Amsterdam')
    Main_Data['day'] = Main_Data['ts'].dt.day
    Main_Data['hour'] = Main_Data['ts'].dt.hour
    Main_Data['minute'] = Main_Data['ts'].dt.minute
    Main_Data['second'] = Main_Data['ts'].dt.second
    #the database start from 23.59 from the day before so all the data start from
    #yesterday are all zero
    if no ==1:
        Main_Data['second']=(Main_Data.day!=31)*Main_Data.second
        Main_Data['minute']=(Main_Data.day!=31)*Main_Data.minute
        Main_Data['hour']=(Main_Data.day!=31)*Main_Data.hour
    elif no!=1:
        Main_Data['second']=(Main_Data.day!=(no-1))*Main_Data.second
        Main_Data['minute']=(Main_Data.day!=(no-1))*Main_Data.minute
        Main_Data['hour']=(Main_Data.day!=(no-1))*Main_Data.hour
    
    #new dataset and indexing fid
    Main_Data=Main_Data[["fid",'alt','day','hour','minute','second','roc']]
    Main_Data=Main_Data.set_index(['fid'])

    M=Main_Data
    #sort by the fid
    M=M.sort_index()
    #Taking the aircraft that has altitude >0 and rate of climb =0
    M=M[M.alt !=0].drop(['alt'],axis=1)
    M=M[M.roc ==0].drop(['roc'],axis=1)

    #converting hour and miuntes into second then add it to second column
    M['second']=M['minute']*60 +M['hour']*60*60+M['second']

    #Find difference the max and min in second column
    #to find the flight duration of that aircraft with the signal range.
    max1=M.groupby(by=['fid'])['second'].max()
    min1=M.groupby(by=['fid'])['second'].min()
    dif=max1-min1
    
    return dif

def other(df):
    #Now i am setting up all the models that has less than 1 percent
    #calculating percentage for each model
    data=df/(df.sum()) *100
    #limit percentage
    percent=1
    #all the model that is more than 1 %
    data1=data[data>percent]
    #all the model that is less than 1%
    data2=data[data<percent]
    #summing all the model that is less than 1% then added to the list
    data3=data1.T
    data3['others']=data2.sum()
    data=data3.T
    #just making colorfull pie chart
    color = cm.gist_rainbow((np.arange(len(data)))/(len(data)))
    return data,color

list1=[]
#reading and filtering all the data for the whole month
for i in range(1,32):
    if i<10:
        print(i)
        file = str('ADSB_combined_2018010'+ str(i) + '.csv')
        main=main_data(file,i)
        list1.append(main)

    else:
        print(i)
        file = str('ADSB_combined_201801'+ str(i) + '.csv')

        main=main_data(file,i)
        list1.append(main)


# the main data after filtered
#Main=pd.DataFrame(list1,columns=['day','mean time'])
t=pd.concat(list1,axis=1,sort=False)
print(t)
t.to_csv(str('Record_time_spent with ROC.csv'))

