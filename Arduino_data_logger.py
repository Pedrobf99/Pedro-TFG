# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:28:28 2022

@author: Admin
"""
import serial
#import time

port="COM19" #nombre del puerto al que se conecta el arduino
baud=9600 #ratio del arduino

filename="Datos_tfg.csv" #Archivo guardar datos

n_filas=20 #numero de datos maximos para almacenar

file=open(filename,"w")


ser=serial.Serial(port,baud) #conexion con el arduino
measures=0
while measures<n_filas:

    getData=str(ser.readline())
    #print(getData)
    
    #print("FILAS")
    fila=getData[0:][2:-3]
    
    print(fila)
    
    measures=measures+1
    
    
    file = open(filename, "a") #añadimos informacion al archivo
    file.write(fila + "\n") #escribimos cada linea
    
file.close() #cerramos el archivo
ser.close() #cerramos el puerto