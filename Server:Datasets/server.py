#!/usr/bin/python
# coding=utf-8
# import urlparse
import xmlrpclib
import csv
import pandas as pd 
from furl import furl
# import datetime

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import parse_qsl, urlparse
from operator import itemgetter


data = pd.read_csv("Habitantes 2015.csv") 
data2 = pd.read_csv("DELITOS.csv")
PORT_NUMBER = 8084

#This class will handles any incoming request from the browser 
class HTTPHandler(BaseHTTPRequestHandler):
    global reader
    def territorio(self):
        t = {}
        for index, row in data.iterrows():
            m=row['MUNICIPIOS'].replace("Ñ", "N")
            q=float(row['Extensión Territorial (km2)'])
            municipio = {m:q}   
            t.update(municipio)
        return t

    def poblacion(self):
        p = {}
        for index, row in data.iterrows():
            m=row['MUNICIPIOS'].replace("Ñ", "N")
            q=float(row['Población 2015'])
            municipio = {m:q}
            p.update(municipio)
        return p

    def densidad(self):
        d = {}
        for index, row in data.iterrows():
            m=row['MUNICIPIOS'].replace("Ñ", "N")
            q=float(row['Densidad de Población (hab/km2)'])
            municipio = {m: q}
            d.update(municipio)
        return d

    def delitosMunicipio(self,year):

        data2['MUNICPIOS'] = data2['MUNICPIOS'].str.replace('Ñ','N')
        municipios = data2['MUNICPIOS'].unique()
        municipios = municipios [:-1]
        tuplas={}

        for m in municipios:
            totalDelitos = (data2.loc[data2['MUNICPIOS']==m,'ENE-DIC '+str(year)]).convert_objects(convert_numeric=True).sum()
            tupla = {m:totalDelitos}
            tuplas.update(tupla)
        return tuplas
        
    def delitosEsp(self,year):
        data2['Delito'] = data2['Delito'].str.replace('ó','o')
        data2['MUNICPIOS'] = data2['MUNICPIOS'].str.replace('Ñ','N')
        municipios = data2['MUNICPIOS'].unique()
        municipios = municipios [:-1]
        tipos = data2['Delito'].unique()
        tipos = tipos [:-1]
        tuplas={}
        for m in municipios:
            tipo = data2.loc[data2['MUNICPIOS']==m,['Delito','ENE-DIC '+str(year)]]
            tipo = tipo.to_dict('records')
            tuplas[m]={}
            for delito in range(0,len(tipo)):
                tuplas[m][tipo[delito]['Delito']]= float(str(tipo[delito]['ENE-DIC '+str(year)]))
              
        return tuplas
       
    def delitosYear(self,year):
        data2['Delito'] = data2['Delito'].str.replace('ó','o')
        data2['MUNICPIOS'] = data2['MUNICPIOS'].str.replace('Ñ','N')
        delitos = data2['Delito'].unique()
        delitos = delitos [:-1]
        data2['ENE-DIC '+str(year)]= data2['ENE-DIC '+str(year)].convert_objects(convert_numeric=True)
        tuplas = {}
        for d in range(len(delitos)):
            x = data2.groupby('Delito').sum().to_dict()
            x['ENE-DIC '+str(year)][delitos[d]]
            tupla = {delitos[d]: x['ENE-DIC '+str(year)][delitos[d]]}
            tuplas.update(tupla)
        return tuplas
    
    def getRegressionData(self):
        data3 = pd.read_csv('regression2.csv')
        X_val = data3['DENSIDAD_POBLACION']
        Y_val = data3['NUM_DELITOS']
        
        regression = []

        for i in range(0,len(X_val)):
            regression.append([X_val[i],Y_val[i]])
        
        return regression

    def getPrediction(self):
        pred = pd.read_csv('prediction.csv')
        return pred.values.tolist()
            

    def do_GET(self)  :
    
        ### HANDLE DIFFERENT GET PATHS IN URL (ENDPOINTS)
         
        if self.path == '/territorio':
            t = self.territorio()
        
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(t)

        elif self.path == '/poblacion':
            p = self.poblacion()
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(p)

        elif self.path == '/densidad':

            d = self.densidad()
        
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(d)

        elif self.path.startswith('/delitosMunicipio?') :

            params = furl(self.path)
            year = params.args['year']
            d = self.delitosMunicipio(year)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(d)
        
        elif self.path.startswith('/delitosEsp?') :

            params = furl(self.path)
            year = params.args['year']
            d = self.delitosEsp(year)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(d)

        elif self.path.startswith('/delitosYear?') :

            params = furl(self.path)
            year = params.args['year']
            d = self.delitosYear(year)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(d)

        elif self.path.startswith('/getRegressionData?') :

            params = furl(self.path)
            index = params.args['index']
            d = self.getRegressionData(index)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(d)
        
        elif self.path == '/getRegressionData':
            p = self.getRegressionData()
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(p)


        elif self.path == '/getPrediction':
            p = self.getPrediction()
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(p)
        return
   
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), HTTPHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()