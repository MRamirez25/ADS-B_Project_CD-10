import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
pd.set_option('display.max_columns', 13)
pd.set_option('display.width', 500)


def main_data (file):
    ####    open the files and give type of column data
    Main_Data = pd.read_csv(file,
                            dtype={"ts": object, "icao": object, "lat": float, "lon": float, "alt": float,
                                   "gs": float, "trk": float, "roc": float, "callsign": object, "fid": object,
                                   "regid": object, "mdl": object, "type": object, "operator": object})
    print('Done with Data')
    Main_Data=Main_Data[['lat','lon',"alt","mdl", "fid",'roc']]
    Main_Data = Main_Data[(Main_Data["lat"] >= 50.50) & (Main_Data["lat"] <= (53.5)) & (Main_Data["lon"] >= 3.5) & (Main_Data["lon"] <= (7))]

    Main_Data=Main_Data[["alt","mdl", "fid",'roc']]
    #Taking all the aircraft that has rate of climb==0
    Main_Data=Main_Data[Main_Data.roc ==0].drop(['roc'],axis=1)

    
    #If the altitude >0: True and the altitude<=0 : False
    Checker=(Main_Data['alt']!=0)
    #adding data b into the main database
    new_data=Main_Data.join(Checker, rsuffix='_bool')
    #removing all the plane that has altitude =0
    new_data=new_data[new_data.alt_bool !=False]

    
    #setting up indexs
    new_data=new_data.set_index(['mdl','fid'])
    #grouping fid and model of aircraft
    #Then setting each unique combination as one [--> .apply(lambda x:1]]
    new_data1=(new_data.groupby(by=['fid','mdl'])['alt_bool'].count()).apply(lambda x:1)

    #creating new database 
    new_data=pd.DataFrame(new_data1)
    #naming the columns
    new_data=new_data.rename(columns={'alt_bool':'Number of aircraft'})
    #grouping fid and counting all the fid that has same models 
    M=new_data1.groupby(level=1).count()

    return pd.DataFrame(M)

def other(df):
    #setting up all the models that has less than 1 percent
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

listofModels=[]
#reading and filtering all the data for the whole month
for i in range(1,32):
    if i<10:
        print(i)
        file = str('ADSB_combined_2018010'+ str(i) + '.csv')
        main=main_data(file)
        main=main.rename(columns={'alt_bool':str('day '+str(i))})
        listofModels.append(main)
        print(main)
    else:
        print(i)
        file = str('ADSB_combined_201801'+ str(i) + '.csv')

        main=main_data(file)
        main=main.rename(columns={'alt_bool':str('day '+str(i))})
        listofModels.append(main)

# the main data after filtered
Main=pd.concat(listofModels,axis=1,sort=False)


#calculating the mean of each models for the whole month
mean=Main.T.mean()
mean1,cs=other(mean)
#creating pie chart 
mean1.plot(kind='pie',wedgeprops=dict( edgecolor='w'),autopct='%1.1f%%',labeldistance=1.1,pctdistance=0.9,rotatelabels=True,colors = cs)
plt.ylabel("Model of aircrafts")

Total=Main.T.sum()
#new table for mean + percentage total that are active
Main_data1={'Mean Total':mean,
           'Percentage':Total/(sum(Total)) *100}
Main_data=pd.DataFrame(Main_data1)
Main_data=Main_data.round(3).fillna(value=0)
Main_data.sort_index()
print(Main_data)

Main_data.to_csv(str('TrafficMix_decribe_model_one_month.csv'))
plt.show()
