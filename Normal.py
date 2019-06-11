# -*- coding: utf-8 -*-
"""
Created on Tue May  7 15:53:40 2019

@author: Frank
"""
import pandas as pd
import numpy as np
import scipy.stats as sc
import matplotlib.pyplot as plt

xrange1 = 501
xrange2 = 121

Mean = pd.read_csv('Mean_Count_Runway_January.csv')
Var = pd.read_csv('Variance_Count_Runway_January.csv')
Mean = Mean.set_index('Unnamed: 0')
Var = Var.set_index('Unnamed: 0')

Color = ['C1','C2','C3','C4','C5','C6','C7','C8','C9']
Markers = ['o','^','s','+','D','x']
Markers_on1 = np.arange(0,xrange1,10)
Markers_on2 = np.arange(0,xrange2,10)

Mean1 = Mean.drop(['Eindhoven','Oostbaan','Rotterdam','Maastricht'])
Var1 = Var.drop(['Eindhoven','Oostbaan','Rotterdam','Maastricht'])

Mean2 = Mean.drop(['Maastricht','Aalsmeerbaan','Buitenveldertbaan','Kaagbaan','Polderbaan','Zwanenburgbaan'])
Var2 = Var.drop(['Maastricht','Aalsmeerbaan','Buitenveldertbaan','Kaagbaan','Polderbaan','Zwanenburgbaan'])


for i in range(Mean1.shape[0]):
    n1dist = sc.norm.pdf(np.arange(xrange1), Mean1.iloc[i], np.sqrt(Var1.iloc[i]))
    l1 = plt.plot(np.arange(xrange1), n1dist, str('-'+Color[i]+Markers[i]), markevery=20, linewidth=2)

    plt.legend(Mean1.index)
    plt.xlabel('Number of flights')
    plt.ylabel('Probability density')
    plt.savefig('Runway_normal_1.pdf', format='pdf')
plt.show()


for j in range(Mean2.shape[0]):
    n2dist = sc.norm.pdf(np.arange(xrange2), Mean2.iloc[j], np.sqrt(Var2.iloc[j]))
    l2 = plt.plot(np.arange(xrange2), n2dist,  str('-'+Color[j]+Markers[j]), markevery=5, linewidth=2)
    plt.legend(Mean2.index)
    plt.xlabel('Number of flights')
    plt.ylabel('Probability density')
    plt.savefig('Runway_normal_2.pdf', format='pdf')
plt.show()
