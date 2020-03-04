import pandas as pd
from pandas import read_csv
import matplotlib.pylab as plt
from matplotlib import pyplot
import csv


PA = pd.read_csv('ACCESO'+'.csv',  parse_dates=[0], header=None,index_col=0, squeeze=True, names=['fecha','Total_Informatica','ble'])
PAInfor=PA.resample('D').max()
PAInfor=PAInfor['Total_Informatica']
df = pd.read_csv('AEMET'+'.csv',  parse_dates=[0], header=None,index_col=0, squeeze=True, names=['fecha','vis', 'dv', 'stddv','vv', 'alt', 'vmax', 'lon', 'ts', 'prec', 'tamax', 'pres','ta','tss5cm', 'hr', 'inso', 'lat', 'dmax', 'tamin', 'pacutp', 'stdvv', 'tpr', 'press_nmar', 'tss20cm'])
ta_ext_diaria=df['ta'].resample('D').mean()
hum_diaria=df['hr'].resample('D').mean()

rf=pd.read_csv('AseoInfor.csv',  parse_dates=[0], header=None,index_col=0, squeeze=True,names=['fecha','Informatica', 'me'])
xf=pd.read_csv('AeosFem.csv',  parse_dates=[0], header=None,index_col=0, squeeze=True,names=['fecha','Informatica', 'me'])
rf=rf.resample('D').sum()
xf=xf.resample('D').sum()
consumo_agua=rf['Informatica']*10
print(consumo_agua)

tf=pd.read_csv('TEMPINF.csv',  parse_dates=[0], header=None,index_col=0, squeeze=True,names=['fecha','Humedad','VBAT', 'Temperatura'])
tf=tf.resample('D').mean()
t_pab_diaria=tf['Temperatura']
h_pab_diaria=tf['Humedad']
rf=pd.concat([consumo_agua,ta_ext_diaria, hum_diaria, t_pab_diaria, h_pab_diaria, PAInfor], ignore_index=True, axis=1, names=['Consumo Litros', 'T ambiental diaria','humamb_diaria', 'Temperatura Informatica diaria', 'Humedad Informatica diaria', 'Conexiones punto acceso diarias'])
data=pd.concat([consumo_agua, PAInfor], ignore_index=True, axis=1, names=['Consumo Litros', 'Conexiones punto acceso diarias'])
m = csv.writer(open('dataseo.csv', 'w'))

export_csv= data.to_csv ('dataseo.csv', index = 3, header=True)

r = csv.writer(open('dataset.csv', 'w'))

export_csv= rf.to_csv ('dataset.csv', index = 3, header=True)


train=pd.read_csv('dataset.csv',  parse_dates=[0], header=None,index_col=0, squeeze=True,names=['fecha','Consumo diario','Temperatura Ambiental','humamb_diaria', 'Temperatura Pabellon', 'Humedad', 'PA'])
correlaciones=train.corr(method="pearson")

correlaciones = correlaciones["Consumo diario"].sort_values(ascending=False)





data = data['2018-12-14':]
data['Consumo']=data[0]
data=data.drop([0], axis=1)
data['Conexiones']=data[1]
data=data.drop([1], axis=1)
data['Consumo'].fillna(0, inplace=True)
data['Conexiones'].fillna(0, inplace=True)

correlaciones=data.corr(method="pearson")
correlaciones=correlaciones['Consumo'].sort_values(ascending=False)
data.to_csv('red.csv')
dataset=read_csv('red.csv', header=0, index_col=0)
print(correlaciones)
values= dataset.values

groups=[0,1]
i=1
pyplot.figure
for group in groups:
    pyplot.subplot(len(groups), 1, i)
    pyplot.plot(values[:, group])
    pyplot.title(dataset.columns[group], y=0.5, loc='right')
pyplot.show()

#correlaciones = correlaciones["Consumo Litros"].sort_values(ascending=False)
#print(correlaciones)
"""
df = pd.read_csv('UEXCC_INV_P00_CUA016_SEN004_AGU.csv',  parse_dates=[0], header=None,index_col=0, squeeze=True,names=['fecha','unidades'])
maxdia=df.resample('D').max()
print(maxdia[maxdia.index.dayofweek < 5])
#print(maxdia)
f = csv.writer(open('totalepccdias.csv', 'w'))
export_csv = maxdia.to_csv ('totalepccdias.csv', index = 2, header=True) #Don't forget to add '.csv' at the end of the path


totalmeses=maxdia.resample('M').sum()
#print(totalmeses)
r = csv.writer(open('totalepccMESES.csv', 'w'))
export_csv = totalmeses.to_csv ('totalepccMESES.csv', index = 2, header=True) #Don't forget to add '.csv' at the end of the path
"""