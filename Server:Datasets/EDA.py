# coding=utf-8
import csv
import pandas as pd 
from operator import itemgetter

data = pd.read_csv("Habitantes 2015.csv") 
data2 = pd.read_csv("DELITOS.csv")

def territorio():
    t = {}
    for index, row in data.iterrows():
        municipio = {row['MUNICIPIOS']:row['Extensión Territorial (km2)']}   
        t.update(municipio)
    return t

def poblacion():
    p = []
    for index, row in data.iterrows():
        municipio = {row['MUNICIPIOS']: row['Población 2015']}
        p.update(municipio)
    return p

def densidad():
    d = {}
    for index, row in data.iterrows():
        m=row['MUNICIPIOS'].replace("Ñ", "N")
        municipio = {m: row['Densidad de Población (hab/km2)']}
        d.update(municipio)
    d = sorted(tuplas.items(), key=itemgetter(-1), reverse=True)
    return d

def delitosYear(year):
   
   
    data2['Delito'] = data2['Delito'].str.replace('ó','o')
    delitos = data2['Delito'].unique()
    delitos = delitos [:-1]
    tuplas={}
    data2.drop(data2.tail(1).index,inplace=True) 
    
    
        

   

def delitosMunicipio(year):

    data2['MUNICPIOS'] = data2['MUNICPIOS'].str.replace('Ñ','N')
    municipios = data2['MUNICPIOS'].unique()
    municipios = municipios [:-1]
    tuplas={}

    for m in municipios:
        totalDelitos = (data2.loc[data2['MUNICPIOS']==m,'ENE-DIC '+str(year)]).convert_objects(convert_numeric=True).sum()
        tupla = {m:totalDelitos}
        tuplas.update(tupla)

    tuplas=sorted(tuplas.items(), key=itemgetter(-1), reverse=True)

    return tuplas


#print delitosMunicipio(2013)
delitosYear(2013)
