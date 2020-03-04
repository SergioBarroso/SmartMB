import requests
import os, sys
import json
import datetime
import csv
import pandas as pd
import matplotlib.pylab as plt

fechainicio='10-01-2016T00:00:00Z'
fechafinal='24-02-2020T00:00:00Z'
nameofsensor='UEXCC_INV_P00_CUA016_SEN009_APC'

fechainicio = datetime.datetime.strptime(fechainicio, "%d-%m-%YT%H:%M:%SZ")
fechafinal = datetime.datetime.strptime(fechafinal, "%d-%m-%YT%H:%M:%SZ")

contador= 0
ffmod = 0
content=[]
while ffmod != fechafinal:
    fimod = fechainicio + datetime.timedelta(days=contador)#timedelta lo que hace es aumentar en este caso los dias el valor que indiques, en la primera iteracción contador a 0 para que analice el dia correspondientes
    ffmod = fechainicio + datetime.timedelta(days=contador + 1)
    r = requests.get('http://158.49.112.127:11223/read/influx/json?json={"info": {"api_key": "000000","device": "'+ nameofsensor + '","from":"'+fimod.strftime("%Y-%m-%dT%H:%M:%S")+'", "to":"'+ffmod.strftime("%Y-%m-%dT%H:%M:%S")+'"}}') #url de llamada al servicio
    try:
        content = content+json.loads(r.content)
        contador += 1
    except:
        contador+=1
with open(nameofsensor+'.json', 'w') as file:
    json.dump(content, file, indent=4)

with open(nameofsensor+'.csv', 'w', newline='') as csvfile:
    f= csv.writer(csvfile, delimiter=',',
                         quoting=csv.QUOTE_ALL)
    for item in content:
        #hola=list(item['data'].values())
        hola=item['data']['Total_Total']
        header = [item['created_at']]
        """
        for i in hola:
            header.append(i) if type(i)==int or type(i)==float else contador
        """
        header.append(hola)
        f.writerow(header)



#print(maxdia)
#print(maxdia[maxdia.index.dayofweek < 5])