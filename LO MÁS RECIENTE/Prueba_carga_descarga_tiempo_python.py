# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:28:28 2022

@author: Admin
"""
import serial
#import numpy as np
import time
#import matplotlib.pylab as plt

folder="Datos/"

port="COM19" #nombre del puerto al que se conecta el arduino
baud=115200 #ratio del arduino

ser=serial.Serial(port,baud) #conexion con el arduino

    
#Preguntas para guardar los datos de forma ordenada
chip=input("¿Que chip estamos midiendo? ")
condiciones=input("¿Bajo iluminación? (Y/N) ")
estructura=input("¿NCAP, MIM, PCAP? (Out en 1,2,11) ")

#Construir el nombre del archivo donde guardar los datos
if estructura=="1":
    estructura="NCAP"
elif estructura=="2":
    estructura="MIM"
elif estructura=="11":
    estructura="PCAP"
    
if condiciones=="Y" or condiciones=="Si" or condiciones=="si":
    luz=input("Alguna característica de la luz:")
    filename="Datos_"+chip+"_"+estructura+"_luz_"+luz+".csv" #Archivo guardar datos
else:
    filename="Datos_"+chip+"_"+estructura+"_sinluz.csv"  #Archivo guardar datos



file=open(folder+filename,"w")

t_measures=0
measures=0
fallito=0
fallos=[]
filas=[]
dts=[]
times=[]

#Primer mensaje del arduino va aser cuantas medidas va a hacer por memoria
medi=str(ser.readline())
while "Medidas" not in medi:
    medi=str(ser.readline())

repeticiones=str(ser.readline()) #Número de veces que vamos a leer cada memoria

n=int(repeticiones[0:][2:-5])
print(n)
n_filas=n*32 #numero de datos maximos para almacenar 

file = open(folder+filename, "a") #añadimos informacion al archivo

file.write("Lectura analógica,Tiempo\n")
file.write(str(n)+","+str(n) + "\n") #escribimos numero de medidas por memoria

#siguiente mensaje será el comienzo de datos de la primera medida
start=str(ser.readline().decode())
while "SuperInicio" not in start:
    start=str(ser.readline().decode())
print(start[0:-2])

time_start=time.time()

#Ahora almacenamos los valores que el arduino envía durante un ciclo completo    
while t_measures<n_filas:

    getData=ser.readline()
    #print(getData)
    
    
    fila=getData.decode()[0:][0:-2]
    #print(fila)  
    
    if str(getData).find('Inicio')==-1 and str(getData).find('Final')==-1:
        #Cada fila representa los valores de una FILA DE MEMORIAS (fijando la columna y si es sel o seln)
        #print(fila)  
        t_medida=time.time()-time_start
        times.append(t_medida)
        filas.append(fila)
        try:
            dts.append(float(filas[t_measures]))    #en esta matriz almacenamos los valores de todas las memorias (cada memoria esta separada por 32 valores)
        except:
            dts.append(float(filas[t_measures-32]))    #en el caso de que haya un error tomamos el último valor que hayamos medido de esa memoria

        file.write(str(dts[t_measures])+","+str(times[t_measures])+"\n") #escribimos cada linea
        t_measures=t_measures+1
        
    else:
        print(fila)
        measures=measures+1
        
    
    

print("Hubo "+str(fallito)+" fallito(s) en la(s) posicion(es): "+ str(fallos))
print("El archivo de datos es: " + filename)
print("measures: " +str(measures)+" t_measures: "+str(t_measures))
#print(dts) #Esta es la matriz con la que podemos analizar los datos directamente en python
file.close() #cerramos el archivo
ser.close() #cerramos el puerto











"""
a=[] #Matriz auxiliar
b=[] #Datos de cada memoria ordenados fila a fila
t1=[] #Matriz auxiliar
t_final=[] #Tiempos de cada memoria ordenados fila a fila

for j in range(0,32):
    for i in range(0,n):
        a.append(dts[i*32+j]*3.3/1024)
        t1.append(times[i*32+j])
    b.append(a[j*n:j*n+n])
    t_final.append(t1[j*n:j*n+n])

# plot with various axes scales
plt.figure()

# Primera fila de memorias
plt.subplot(221)
for i in range(0,4):
    plt.plot(b[i],t_final[i])

plt.ylabel('Lectura analógica (V)')
plt.title('Primera fila de memorias')
plt.grid(True)

# Segunda fila de memorias
plt.subplot(222)
for i in range(4,8):
    plt.plot(b[i],t_final[i])

plt.title('Segunda fila de memorias')
plt.grid(True)

# Tercera fila de memorias
plt.subplot(223)
for i in range(8,12):
    plt.plot(b[i],t_final[i])

plt.ylabel('Lectura analógica (V)')
plt.xlabel('Tiempo (ms)')
plt.title('Tercera fila de memorias')
plt.grid(True)

# Cuarta fila de memorias
plt.subplot(224)
for i in range(12,16):
    plt.plot(b[i],t_final[i])

plt.xlabel('Tiempo (ms)')
plt.title('Cuarta fila de memorias')
plt.grid(True)

# Adjust the subplot layout, because the logit one may take more space
# than usual, due to y-tick labels like "1 - 10^{-3}"
#plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)

plt.show()

"""
