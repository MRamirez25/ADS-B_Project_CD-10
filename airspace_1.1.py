
from multiprocessing import Process, Pool
import pandas as pd
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from matplotlib import cm
from math import log10
import time



def avg_calculator(time_len_res_start,time_len_res,long_res,lat_res,timestep,main_df1,day,our): #this funtion makes a 2d list of avarage values of the differen squeres

    main_df = pd.read_csv(main_df1[0],
                        dtype={"ïnd" : int, "ts": float, "icao": str, "lat": float, "lon": float, "alt": float,}) #importing the databace
    
    main_df['ts'] = main_df['ts'].apply(lambda x: x - (48*365*24*60*60 + 12*24*60*60 - 3600)) #adjusting time

    airspace_df1 = main_df[['ts','lat','lon','icao',"alt"]]
    airspace_df1 = airspace_df1[((airspace_df1["ts"]) <= (time_len_res*timestep + timestep *2 + 30)) & ((airspace_df1["ts"]) >= (time_len_res_start*timestep - 11)) & (airspace_df1["lat"] >= 50.50) & (airspace_df1["lat"] <= (53.5)) & (airspace_df1["lon"] >= 3.5) & (airspace_df1["lon"] <= (7)) & (airspace_df1["alt"] >= 400)]

    x = -1
    y = -1
    z = -1
    i = 0

    list4 = []
    list3 = []
    list_contr = []
    days = 31
    liststr = day_str_cr(days)
    for time1 in range(time_len_res_start,time_len_res,100):
        airspace_df2 = airspace_df1[(airspace_df1['ts'] >= time1*timestep) & (airspace_df1['ts'] <= (time1+100)*timestep)]
        
        list6 = []
        for time in range(time1,(time1+100)):
            z = z + 1

            list2 = []
        
            airspace_df2 = airspace_df1[(airspace_df1['ts'] >= time*timestep) & (airspace_df1['ts'] <= (time+1)*timestep)]
            val1 = airspace_df2.icao.nunique()
            total1 = 0
            for lon in np.arange (3.5,7,long_res):
                airspace_df = airspace_df2[(airspace_df2['lon'] >= lon) & (airspace_df2['lon'] <= lon+long_res)]

                list1 = []

                for lat in np.arange (50.50,53.5,lat_res):

                    airspace_sub_df = airspace_df[(airspace_df["lat"] >= lat) & (airspace_df["lat"] <= (lat+lat_res))]
                    val = airspace_sub_df.icao.nunique() #this count how many differnt icao the are in a square
                    total1 = total1 + val
                    list1.append(val)

                list2.append(list1)
            if total1 == 0:
                cor = 0
            else:
                cor = (val1/total1)
            list2 = [[j*cor for j in i] for i in list2]
            list3.append(list2)
            
            

        list6 = list6 + list3
    list4 = []
    list7 = []
    list8 = []
    print (list6)
    list_max1 = []
    print(len(list1),len(list2),len(list2))
    for g in range(len(list2)):
        list5 = []
        for f in range(len(list1)):
            total = 0
            total1 = 0
            for k in range(len(list3)):
                val = list6[k][g][f]
                total = total + val*timestep/(long_res*lat_res)
            
            avg = total/(timestep*(time_len_res-time_len_res_start))    #calculates of a square over multiple timestamps 
            if avg == 0:
                avg = 0
                avg1 = 0
            else:
                avg1 = avg
                avg = avg
                
            for j in range(len(list3)):
                val = list6[j][g][f]
                total1 = total1 + ((val*timestep/(long_res*lat_res)) - avg1)**2 
            avg3 = (total1/(timestep*(time_len_res-time_len_res_start)))**0.5
            
            list7.append(avg3)
            list5.append(avg)
        list_max1.append(max(list5))
        list4.append(list5)
        list8.append(list7)
    max1 = max(list_max1)

    day = main_df1[1]
    file = open(liststr[our][day],"w+")# a file is created here
    file.write(str([list4,max1])) #the list is whritten into the file here
    file.close()
    return list4, list8,max1,len(list1), len(list3)






def time_of_day(time_len_res_start,time_len_res,long_res,lat_res,timestep,main_df1,nu): #this function will make the 2 list for mulitple hours
    listtotal = []
    listmax = []
    list4 = []
    maxlist = []
    processlist = []
    days = 1
    for j in range(24):
        i = main_df1[1] - 1
        nu = j
        
        set1 = avg_calculator(int(time_len_res_start + (i*86400)/timestep + (nu*60*60)/timestep),int(time_len_res + (i*86400)/timestep +((nu*60*60)/timestep)),long_res,lat_res,timestep,main_df1,i,nu)
        listtotal.append(set1[0])
        listmax.append(set1[2])
    for g in range(len(listtotal[0])):
        list5 = []
        for f in range(len(listtotal[0][0])):
            total = 0
            total1 = 0
            for k in range(len(listtotal)):
                val = listtotal[k][g][f]
                total = total + val*(long_res*lat_res)
                    
            
            avg = total/days
            list5.append(avg)

    
        list4.append(list5)
        maxlist.append(max(list5))
    max1 = max(maxlist)

    print (maxlist)
    print (list4)
    return list4,0,max1

def makeplt(l,i): #this can make a plot 
    colar_res = 20

    viridis = cm.get_cmap("viridis",256)
    fig, axs = plt.subplots(1,2, figsize=(6,3),constrained_layout=True)
    for [ax, cmap] in zip(axs, [viridis, viridis]):
            psm = ax.pcolormesh(l[0], cmap=cmap, rasterized=True, vmin=0, vmax=l[2])
            fig.colorbar(psm, ax=ax)

    plt.show()

def do_thing(main_df2): #This finction cals the time_of_day funtion is is easier for the multiprocessing
    days = 5
    i = 1
    cal = time_of_day(0,600,0.09,0.09,6,main_df2,i)
    return cal
    
    print (cal)

def day_str_cr(days1): #this creates names for the files
    list1 = []
    for i in range(24):
        list2 = []
        for j in range(days1):
            string = str(str(j)+","+str(i)+".txt" )
            list2.append(string)
        list1.append(list2)
    return list1
    
if __name__ == '__main__':

    
    filelist = [["ADSB_TimeInterval_20180111.csv",11],["ADSB_TimeInterval_20180112.csv",12],["ADSB_TimeInterval_20180113.csv",13],["ADSB_TimeInterval_20180114.csv",14],["ADSB_TimeInterval_20180115.csv",15],["ADSB_TimeInterval_20180111.csv",11],["ADSB_TimeInterval_20180112.csv",12],["ADSB_TimeInterval_20180113.csv",13],["ADSB_TimeInterval_20180114.csv",14]]

    processes = []
    dayr = 1
    liststr = day_str_cr(dayr)
    i = range(4)
    p = Pool()  #this makes it posible to use python on multiple cores 
    print("hoi1")
    result = p.map(do_thing, filelist)
    print("hoi2")
    p.close()
    p.join()
    print("hoi3")
    o = 0
    print (result)
    for l in result:
        o = o + 1
        makeplt(l,o)
    









