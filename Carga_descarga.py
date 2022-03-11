# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 14:13:52 2022

@author: Admin
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:28:28 2022

@author: Admin
"""
import serial
#import numpy as np
import time
import matplotlib.pylab as plt

folder="Datos/"

port="COM19" #nombre del puerto al que se conecta el arduino
baud=115200 #ratio del arduino

filename="Datos_tfg.csv" #Archivo guardar datos

n_filas=1000 #numero de datos maximos para almacenar (dos matrices contando con Inicio y Final)

file=open(folder+filename,"w")


ser=serial.Serial(port,baud) #conexion con el arduino

#Variables usadas para almacenar valores, bucles o contar fallos
filas=[]
dts=[]
times=[]
measures=0
fallito=0
out_lim=0


start=str(ser.readline()) #leemos lo que escribe el arduino

while "Inicio" not in start:   #Esperamos a que empieze un ciclo
    start=str(ser.readline())

time_start=time.time()

#Limitamos los datos que vamos a medir aproximadamente para una serie
while measures<n_filas:

    getData=str(ser.readline())
    #print(getData)
    t_medida=time.time()-time_start
    
    
    fila=getData[0:][2:-3]
    #print(fila)
        
    if "Inicio" in fila:
        fila=fila[0:][:-2]
        print("Inicio del bucle carga/descarga en la medida "+str(measures)+" tiempo del bucle "+str(t_medida))

    elif "Final" in fila:
        fila=fila[0:][:-2]
        print("Final del bucle carga/descarga en la medida "+str(measures)+" tiempo del bucle "+str(t_medida))
        

    else: #Para la mayoría de medidas
        try:
            float_fila=float(fila)
            #print(float_fila)
            
            #En el caso de que el arduino envíe dos mensajes juntos o un valor sin sentido
            if float_fila>1024:
                float_fila=filas[measures-fallito-1]
                out_lim=out_lim+1
                
            #Recogemos los valores de voltaje y tiempo
            filas.append(float_fila)
            times.append(t_medida)
            
        #En el caso de que el arduino escriba algo incoherente
        except ValueError: 
            fallito=fallito+1

    #dts.append(filas[measures].split(","))

    measures=measures+1
    
    
    file = open(folder+filename, "a") #añadimos informacion al archivo
    file.write(str(fila) + "\n") #escribimos cada linea

print("Hubo "+str(fallito)+" fallos y en "+str(out_lim)+" casos el arduino se fue del límite")

plt.plot(times,filas)
plt.xlabel('Tiempo')
plt.ylabel('Lectura analógica')

#print(dts) #Esta es la matriz con la que podemos analizar los datos directamente en python
file.close() #cerramos el archivo
ser.close() #cerramos el puerto