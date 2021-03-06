# -*- coding: utf-8 -*-
"""Copy of Copia de TP1 - Real or Not? NLP with Disaster Tweets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HNCzqoBJgGlJYtuN1yGsE00oI-9atF0f

# **TP1 - Real or Not?**

###  **Análisis exploratorio**

![Banner_TP1.png](https://drive.google.com/uc?id=1BPA2RF1SDm9bTs1xZfVUa1VQn932E3wr)
"""

#IMPORT FILES FROM DRIVE INTO GOOGLE-COLAB:

#STEP-1: Import Libraries

# Code to read csv file into colaboratory:
!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

#STEP-2: Autheticate E-Mail ID

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

#STEP-3: Get File from Drive using file-ID

#2.1 Get the file
downloaded = drive.CreateFile({'id':'1RAGDjlzJ6spO5Sq8_x3UTIvxLhKAUBEt'}) # replace the id with id of file you want to access
downloaded.GetContentFile('train.csv') 

#downloaded = drive.CreateFile({'id':'17pAgG9oJRK1bAFWRKkp96__zicG6yUmy'}) # replace the id with id of file you want to access
#downloaded.GetContentFile('test.csv') 

#downloaded = drive.CreateFile({'id':'1u8v51BT7FZggIRD-eo0dQno--0wlxIhA'}) # replace the id with id of file you want to access
#downloaded.GetContentFile('sample_submission.csv')

# Commented out IPython magic to ensure Python compatibility.
#STEP-4: Import Libraries

!pip install ptitprince
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors
import datetime as dt
import scipy as sp
import ptitprince as pt
#from sklearn.cross_validation import train_test_split -- no levanta
# %matplotlib inline
plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('default') # mejoramos esteticamente un poco los gráficos en matplotlib
sns.set(style='whitegrid') # seteando tipo de grid en seaborn

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_selection import SelectKBest
from sklearn import datasets, linear_model

"""### Levantamos archivo **train.csv**

"""

df_train = pd.read_csv(r'train.csv') 
df_train.head(10)

# exporto a excel
df_train.to_excel('df_train_preprocesado.xlsx')

df_train.info()
# las variables 'keyword' y 'location' estan incompletas

# Creo una columna con el cálculo de los caracteres que tiene la columna 'text' y la llamo 'Caracteres'. 
df_train['Caracteres']=df_train['text'].str.len()
#Creo columna con el calculo de las palabras que tiene la columna 'text' y la llamo 'Palabras
palabras=[]
for i in range(len(df_train)):
  palabras.append(len(df_train.loc[i,'text'].split()))
df_train['Palabras']=palabras
# Despues consulto con un head()
df_train.head(20)

# Verificamos la existencia de valores nulos
df_train.isnull().any()

df_train.isnull().sum()

df_train.describe()

# cuento total de tweets analizados
total_tweets=len(df_train)
total_tweets

# verifico cuantos son verdaderos
tweets_verdaderos=(df_train['target']==1).sum()
tweets_verdaderos

# verifico cuantos son fakes
tweets_falsos=(df_train['target']==0).sum()
tweets_falsos

# calculo la probabilidad (casos favorables/sobre casos posibles) → en este casos es equivalente .mean()
probabilidad_tweet_verdadero = np.round((tweets_verdaderos)/(total_tweets),decimals=2)
probabilidad_tweet_verdadero

# calculo la probabilidad (casos favorables/sobre casos posibles) → en este casos es equivalente .mean()
probabilidad_tweet_falso = np.round((tweets_falsos)/(total_tweets),decimals=2)
probabilidad_tweet_falso

"""### **Iniciamos proceso de limpieza de datos**"""

#COnsulto si hay duplicados
df_train['text'].duplicated().any()

#Cuantos duplicados tengo
df_train['text'].duplicated().sum()

# Eliminamos los duplicados
df_train.drop_duplicates(subset='text',keep='first',inplace=True)

#Chequeamos que las dimensiones del DF
df_train['text'].duplicated().any(),df_train.shape

##Agregamos columnas booleanas al df
df_train['Veridico']=df_train['target']==1
df_train['Falso']=df_train['target']==0
## Rankeo mi cantidad de palabras y caracteres por el percentil en forma de percentil
df_train['Percentil: Caracteres']=df_train['Caracteres'].rank(pct=True)
df_train['Percentil: Palabras']=df_train['Palabras'].rank(pct=True)
df_train=df_train.fillna({'keyword': 'Sin keyword','location': 'Sin location'})
df_train.head()

#Hacemos un describe para ver un poco como estan los datos
df_train.describe()

"""# Analisis por cantidad de caracteres y palabras"""

fig=plt.figure(figsize=(14,6))
sns.set_style(style='white')
ax1=fig.add_subplot(121)
ax2=fig.add_subplot(122)
ax1.set_title('Densidad: Cantidad de caracteres por Tweet',fontsize=12,fontweight='bold')
ax1.set_ylabel('Densidad')
ax1.set_xlabel('Palabras')

ax2.set_title('Densidad: Cantidad de palabras por Tweet',fontsize=12,fontweight='bold')
ax2.set_ylabel('Densidad')
ax2.set_xlabel('Caracteres')
sns.distplot(df_train['Caracteres'],hist=True,ax=ax1,color='purple')
sns.distplot(df_train['Palabras'],hist=True,ax=ax2,color='goldenrod')
plt.show()

#Miramos como estan distribuidos nuestros datos segun numero de caracteres y numero de palabras

#Rapidamente miramos nuestros datos 
fig = plt.figure(figsize=(14,6))

ax1=fig.add_subplot(121)
ax2=fig.add_subplot(122)

ax2.set_title('Letter Value Plot: Cantidad de Caracteres de los Tweets')
ax2.set_ylabel('Caracteres')

ax1.set_title('Letter Value Plot: Cantidad de Caracteres de los Tweets')
ax1.set_ylabel('Palabras')
sns.boxenplot(data=df_train,x='Veridico',y='Caracteres',\
                palette='pastel',ax=ax1,width=0.8)
sns.stripplot(data=df_train,x='Veridico',y='Caracteres',\
                ax=ax1,size=1,color='gray')

ax2.set_title('Letter Value Plot: Cantidad de Palabras de los Tweets')
ax2.set_ylabel('Palabras')


sns.boxenplot(data=df_train,x='Veridico',y='Palabras',\
                palette='BrBG_r',ax=ax2,)
sns.stripplot(data=df_train,x='Veridico',y='Palabras',\
                ax=ax2,size=1,color='gray')
plt.show()

#Rainplot de Palabras
plt.figure(figsize=(10,6))
ax=pt.RainCloud(data=df_train,x='Veridico',y='Palabras',\
                orient='h', width_viol = 1.2,cut=0,bw=.1,palette='BrBG_r',height=5)
ax.set_title('Rainplot')
ax.set_xlabel('Palabras')
plt.show()

#Rainplot  Caracteres
plt.figure(figsize=(10,6))
ax=pt.RainCloud(data=df_train,x='Veridico',y='Caracteres',\
                orient='h', width_viol = 1.2,cut=0,bw=.1,palette='BrBG_r',height=5)
ax.set_title('Rainplot')
ax.set_xlabel('Caracteres')
plt.show()

#Me fijo algunos datos estadisticos respecto a mis datos agrupados por su veracidad

grouped_by_veridico=df_train.groupby('Veridico').agg({'Caracteres':['mean','median','std'],'Palabras':['mean','median','std']})
grouped_by_veridico.columns=['Media: caracteres','Mediana: caracteres','Desvio: caracteres','Media: palabras','Mediana: palabras','Desvio: palabras']
grouped_by_veridico=grouped_by_veridico.reset_index()
grouped_by_veridico

"""# Analisis por keyword

**Importamos categorias de los tweets**
"""

#downloaded1 = drive.CreateFile({'id':'1AQR5FKE8mdHD_XTNmMgY_PGmnrGQqu7Q'}) # replace the id with id of file you want to access
#downloaded1.GetContentFile('test.csv')

from google.colab import files
uploaded = files.upload()

import io
categorias = pd.read_csv(io.BytesIO(uploaded[r'df_train_preprocesado.xlsx - categorias_keyword_estadisticas.csv']),usecols=['keyword','palabra clave','Tipo_Desastre'])

# Agrupamos por keyword
data_desastre=df_train.groupby(['keyword']).\
agg({'Caracteres':['mean','median','std'],\
     'Palabras':['mean','median','std'],\
     'Veridico':['mean','sum','std']})
data_desastre=data_desastre.reset_index()
data_desastre.columns=['keyword','Media: caracteres','Mediana: caracteres',\
                                     'Desvio: caracteres','Media: palabras',\
                                     'Mediana: palabras','Desvio: palabras',\
                       'Media: veracidad','Cantidad: veridicos','Desvio: veracidad']
data_desastre

fig=plt.figure(figsize=(8,6))
ax=plt.subplot(111)
ax.set_title('Scatter Plot: Media: caracteres vs Media: veracidad',fontdict={'fontsize':12,'fontweight':1000})
sns.scatterplot(y='Media: caracteres',x='Media: veracidad',data=data_desastre,color='purple',ax=ax)
plt.show()

fig=plt.figure(figsize=(8,6))
ax=plt.subplot(111)
ax.set_title('Scatter Plot: Media: palabras vs Media: veracidad',fontdict={'fontsize':12,'fontweight':1000})
sns.scatterplot(y='Media: palabras',x='Media: veracidad',data=data_desastre,color='purple',ax=ax)
plt.show()

#Veo que tengo fila(categoria) extra de NaN
categorias.tail()

# chequeeamos que estemos eliminando fila que no queremos
categorias.iloc[:-1,:]

#DF limpio
categorias=categorias.iloc[:-1,:]

df_train=df_train.merge(categorias,how='outer',left_on='keyword',right_on='keyword')
df_train.tail()

# Primero miramos cuales son las keywords mas utilizadas
df_train['keyword'].value_counts()

# Agregamos columna al DF que cuente la frecuencia de la keyword y su prob de ser veridica
df_train.loc[:,'Frecuencia: keyword']=df_train.groupby('keyword')['Veridico'].transform('count')
df_train.loc[:,'Probabilidad: keyword']=df_train.groupby('keyword')['Veridico'].transform('mean')

df_train.loc[:,'Prob de veracidad > 0.5']=df_train['Probabilidad: keyword']>0.5
df_train.tail()

# Graficamos una posible relacion entre la frecuencia de una keyword y su probabilidad de ser veridico
plt.figure(figsize=(6,4))

ax=sns.scatterplot(data=df_train,x='Frecuencia: keyword',y='Probabilidad: keyword',color=".0001", marker="+",hue='Prob de veracidad > 0.5')
ax.set_title('Scatter Plot: Frecuencia de Keyword y Probabilidad de que el Tweet sea veridico',fontdict={'fontsize':12,'fontweight':1000})
ax.set_xlabel('Frecuencia de Keyword')
ax.set_ylabel('Probabilidad de veracidad')
sns.set_style('ticks')
ax.legend(loc='upper left', fancybox=True, shadow=True,prop={'size': 8.5})
plt.show()

# Miramos las keywords mas utilizadas, utilizando el percentil 75 como criterio
popular_keywords=df_train['keyword'].value_counts()
popular_keywords=popular_keywords[popular_keywords>np.percentile(popular_keywords,75)]
fig=plt.figure()
ax=plt.subplot(111)
ax.set_title('Barplot: Keyword mas frecuentes',fontdict={'fontsize':12,'fontweight':1000})
popular_keywords.plot(kind='bar',color='purple',figsize=(18,6))
plt.show()

# Miramos las keywords menos utilizadas, utilizando el percentil 25 como criterio
less_popular_keywords=df_train['keyword'].value_counts()
less_popular_keywords=less_popular_keywords[less_popular_keywords<np.percentile(less_popular_keywords,25)]
fig=plt.figure()
ax=plt.subplot(111)
ax.set_title('Barplot: Keyword menos frecuentes',fontdict={'fontsize':12,'fontweight':1000})
less_popular_keywords.plot(kind='bar',color='lightblue',figsize=(18,6))
plt.show()

# Agrupamos keyword por mayor cantidad de tweets veraces
grouped_by_keyword_sort_veridicos=df_train.groupby('keyword').agg({'Veridico':['sum']})
grouped_by_keyword_sort_veridicos.columns=['Tweets Veridicos']
grouped_by_keyword_sort_veridicos=grouped_by_keyword_sort_veridicos.sort_values('Tweets Veridicos',ascending=False)
grouped_by_keyword_sort_veridicos.head()

# Miramos las keywords con mayor catidad de tweets veridicos, utilizando el percentil 75 como criterio
popular_keywords_veridicos=grouped_by_keyword_sort_veridicos.\
loc[(grouped_by_keyword_sort_veridicos['Tweets Veridicos']>np.percentile(grouped_by_keyword_sort_veridicos['Tweets Veridicos'],75))]
popular_keywords_veridicos.head()

# Graficamos las keywords veridicas mas utilizadas
fig=plt.figure(figsize=(12,10))
ax=plt.subplot(111)
ax.set_title('Keywords con mayor cantidad de Tweets veridicos',fontdict={'fontsize':12,'fontweight':1000})
sns.barplot(x=popular_keywords_veridicos['Tweets Veridicos'],y=popular_keywords_veridicos.index,orient='h',ax=ax)

# Agrupamos keywords por tweets falsos
grouped_by_keyword_sort_falso=df_train.groupby('keyword').agg({'Falso':['sum']})
grouped_by_keyword_sort_falso.columns=['Tweets Falsos']
grouped_by_keyword_sort_falso=grouped_by_keyword_sort_falso.sort_values('Tweets Falsos',ascending=False)
grouped_by_keyword_sort_falso.tail()

# Miramos las keywords falsas  mas utilizadas, utilizando el percentil 75 como criterio
popular_keywords_falso=grouped_by_keyword_sort_falso.\
loc[(grouped_by_keyword_sort_falso['Tweets Falsos']>np.percentile(grouped_by_keyword_sort_falso['Tweets Falsos'],75))]
popular_keywords_falso.tail()

# Graficamos las keywords falsas mas utilizadas
fig=plt.figure(figsize=(12,10))
ax=plt.subplot(111)
ax.set_title('Keywords con mayor cantidad de Tweets falsos',fontdict={'fontsize':12,'fontweight':1000})
sns.barplot(x=popular_keywords_falso['Tweets Falsos'],y=popular_keywords_falso.index,orient='h',ax=ax)

# Calculamos cantidad de tweets veridicos por tipo de desastre y su porcentaje de veracidad
porcentaje_desastre_veridico=df_train.groupby('Tipo_Desastre').agg({'Veridico':['sum','mean']})
porcentaje_desastre_veridico.columns=['Veridicos','Porcentaje Veridicos']
porcentaje_desastre_veridico=porcentaje_desastre_veridico.sort_values('Porcentaje Veridicos',ascending=False)
porcentaje_desastre_veridico

# Graficamos tipo de desastre por su porcentaje de veracidad

plt.figure(figsize=(8,6))


ax=sns.barplot(y=porcentaje_desastre_veridico.index,x=porcentaje_desastre_veridico['Porcentaje Veridicos'],orient='h')

ax.set_title('Porcentaje de Tweets Veridicos por Categoria',fontsize=12,fontweight='bold')
ax.set(xlabel='Porcentaje', ylabel='Categoria de Desastre')



plt.show()

# Calculamos cantidad de tweets veridicos por tipo de desastre, agrupamos y aplicamos operaciones para poder usar para grafico stackeado
desastre_veridico=df_train.groupby('Tipo_Desastre').agg({'Veridico':['sum'],'Falso':'sum'})
desastre_veridico.columns=['Veridicos','Falsos']
desastre_veridico=desastre_veridico.stack().to_frame()
desastre_veridico=desastre_veridico.reset_index()
desastre_veridico.columns=['Tipo de Desastre','Tipo de Tweet','Cantidad']
desastre_veridico.sort_values('Cantidad',inplace=True,ascending=False)
desastre_veridico.head()

# Creamos nuevo DF para adicionar columna nueva al Df
y=df_train['Tipo_Desastre'].value_counts().to_frame().reset_index()
y.columns=['Tipo_Desastre','Frec_Categoria']
y.head()

df_train=df_train.merge(y,how='left',left_on='Tipo_Desastre',right_on='Tipo_Desastre')
df_train.head()

# Graficamos tipo de desastre por cantidad de realizaciones falsas y veridicas

fig=plt.figure(figsize=(12,10))
c=sns.catplot(data=desastre_veridico,y='Tipo de Desastre',x='Cantidad',\
              hue='Tipo de Tweet',orient='h',kind='bar',palette='Purples',height=6,aspect=2)
c.fig.suptitle('Cantidad de tweets por categoria del desastre',x=0.5,y=1,fontsize=14,fontweight='bold')
c.set_xlabels('Cantidad')
c.set_ylabels('Categoria de desastre')


plt.show()

"""# Analisis por Location

"""

# Vemos la cantidad de valores no nulos que tenemos: podemos ver que hay muchos
print('Valores no nulos: ',df_train['location'].count())
print('Valores nulos',df_train['location'].isnull().sum())

# Observamos la cantidad de locations que tenemos
location_count=df_train['location'].value_counts()

len(location_count)

# Le pedimos ver cuantas son las locations que solo se repiten una vez
location_unique=location_count[location_count==1]
location_unique.count()

# Vemos que la columna presenta muchos problemas
# Le pedimos muestra aleatoria: Nos arroja valores sin sentido y poco confiables especialmente en los valores con frecuencia=1
example_location=np.random.choice(location_unique.index,40)
example_location

lugar=df_train[['location','target']]

lugar['location'].value_counts()

lugaragrup=lugar.groupby(['location']).agg({'target':['mean','count']})

level0=lugaragrup.columns.get_level_values(0)
level1=lugaragrup.columns.get_level_values(1)
lugaragrup.columns=level0+'_'+level1
lugaragrup.reset_index(inplace=True)

locat=lugar['location']
loca=locat.isnull()

lugar['NaN']=loca

junto=lugar.groupby('NaN').agg({'target':['mean','count']})

duplicado = lugaragrup['target_count'] > 1

lugarduplicado = lugaragrup[duplicado]

unico = lugaragrup['target_count'] <= 1

lugarunico = lugaragrup[unico]

aa = lugarduplicado.plot.scatter(x='target_count',
                      y='target_mean',
                      c='DarkBlue')

print(lugarunico['target_mean'].mean())
print(lugarduplicado['target_mean'].mean())

