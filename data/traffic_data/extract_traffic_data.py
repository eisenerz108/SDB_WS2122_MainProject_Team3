from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XML, fromstring, tostring
import pandas as pd

API_KEY='QCnEQxyPjvejj-6KUBA4y1iTzgpB7SEFiBhE6VGMVdk'
APP_ID = 'U8dDmnjMH5po98oyR2zu'
APP_CODE = '7SWbeiWuI4rSB15ymj52Lg'

page = requests.get('https://traffic.api.here.com/traffic/6.2/flow.xml?app_id='+APP_ID+'&app_code=' +APP_CODE+'&bbox=52.56019067275098, 13.2942200252292;52.506452337674226, 13.431351987442575&responseattributes=sh,fc')
file = open('speeds.txt', "w")
file.write(page.text)
file.close()

soup = BeautifulSoup(open('speeds.txt'))
roads = soup.find_all('fi')

a1=[]
loc_list_hv=[]
lats=[]
longs=[]
sus=[]
ffs=[]
c=0
for road in roads:
    #for j in range(0,len(shps)):
    myxml = fromstring(str(road))
    fc=5
    for child in myxml:
        #print(child.tag, child.attrib)
        if('fc' in child.attrib):
            fc=int(child.attrib['fc'])
        if('cn' in child.attrib):
            cn=float(child.attrib['cn'])
        if('su' in child.attrib):
            su=float(child.attrib['su'])
        if('ff' in child.attrib):
            ff=float(child.attrib['ff'])
    if((fc<=10) and (cn>=0.7)):
        shps=road.find_all("shp")
        for j in range(0,len(shps)):
            latlong=shps[j].text.replace(',',' ').split()
            #loc_list=[]
            la=[]
            lo=[]
            su1=[]
            ff1=[]
            
            for i in range(0,int(len(latlong)/2)):
                loc_list_hv.append([float(latlong[2*i]),float(latlong[2*i+1]),float(su),float(ff)])
                la.append(float(latlong[2*i]))
                lo.append(float(latlong[2*i+1]))
                su1.append(float(su))
                ff1.append(float(ff))
            lats.append(la)
            longs.append(lo)
            sus.append(np.mean(su1))
            ffs.append(np.mean(ff1))


lats_r=[]
longs_r=[]
speeds_r=[]
for i in range(0,len(lats)):
    for j in range(len(lats[i])):
        lats_r.append(lats[i][j])
        longs_r.append(longs[i][j])
        speeds_r.append(sus[i]/ffs[i])
    print(i,len(lats))
    
data_bos=np.array([lats_r,longs_r,speeds_r])
df=pd.DataFrame(data=data_bos[:,1:].T,columns=["latitude", "longitude","speeds"])


speed2=np.array(df['speeds'])
w=np.where(df['speeds']<0.25)
speed2[w]=0
w=np.where((df['speeds']<0.5) & (df['speeds']>0.25))
speed2[w]=1
w=np.where((df['speeds']<0.75) & (df['speeds']>0.5))
speed2[w]=2
w=np.where(df['speeds']>0.75)
speed2[w]=3

df['speeds']=speed2
df.to_csv('df_speeds.csv')