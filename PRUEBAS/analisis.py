# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 00:04:34 2022

@author: Admin
"""
import matplotlib.pylab as plt
#import os 
import pandas as pd
import scipy.optimize as so
import numpy as np
from numpy import *
from numpy.linalg import *

folder="Datos/"
graf="graficas/"
filename="Datos_casita_python6_NCAP_sinluz.csv"

dts=[]
times=[]

# CARACTERISTICAS MEMORIAS
caract=[['4','2','1','0.5'],['4','2','1','6'],['2','1','0.5','4'],['0.5','1','2','4'],
        ['66.32','100.8','206','35.6'],['66.32','100.8','206','35.6'],['0.5','1','2','4'],['4','2','1','6']]
#Variable que cambia en cada caso
var=['Ln','Wn','Lp','Wn','mim','mim','Wn','Wp']

#Leemos todos el archivo filename para representar los datos
dft=pd.read_csv(folder+filename)
arrt=dft.to_numpy()
n=int(arrt[0,0]) #numero de medidas por memoria

for data in arrt[1:,0]:
    dts.append(data)
for data in arrt[1:,1]:
    times.append(data)

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


def simple(t,Vin,a,Vhold):
    return Vin*np.exp(-t/a)+Vhold

def ajuste(t_final,b,bounds):
    
    if bounds:
        coef,cov=so.curve_fit(simple,t_final,b,bounds=bounds)
    else:
        coef,cov=so.curve_fit(simple,t_final,b,bounds=[[0.5,0,0.5],[1.5,0.2,0.65]])
    
    '''
    t1 = np.linspace(0, t_final[-1]*1.1, 100)
    plt.plot(t1,simple(t1,*coef),'r',label='Ajuste $V_C=V_{in}\cdot e^{-t/RC}+V_{HOLD}$')
    #plt.plot(x,y,'o',c='k',label='Resultados del laboratorio')
    
    plt.plot(t_final,b,ls='',marker='o',c='k',label='Datos arduino')
    plt.ylabel('Tiempo (ms)')
    plt.xlabel('$V_{medido} (V)$')
    plt.legend(loc=0,fontsize=8)
    '''
    perr = np.sqrt(np.diag(cov))

    print('Los coeficientes obtenidos del ajuste son: '+str(coef)+' con incertidumbres asociadas: '+str(perr))

    return coef,perr

bounds=[]
valores=[]
Vin=[]
a=[]
Vhold=[]
ln=[4,2,1,0.5]

condiciones=input("Cambiar condiciones? (Y/N) ")
if condiciones=="N":
    for i in range(0,4):
        coefs=ajuste(t_final[i][1:], b[i][1:], bounds)[0]
        
        Vin.append(coefs[0])
        a.append(coefs[1])
        Vhold.append(coefs[2])
    valores.append([Vin,a,Vhold])

else:
    Vinmin=float(input("minimo Vin: "))
    Vinmax=float(input("maximo Vin: "))
    amin=float(input("minimo a: "))
    amax=float(input("maximo a: "))
    Vholdmin=float(input("minimo Vhold: "))
    Vholdmax=float(input("maximo Vhold: "))    
    
    bounds.append([Vinmin,amin,Vholdmin])
    bounds.append([Vinmax,amax,Vholdmax])
    
    for i in range(0,4):
        ajuste(t_final[i][1:], b[i][1:], bounds)

plt.close('all')

fig, axs = plt.subplots(1, 3)
labels=['$V_{in}$','RC','$V_{hold}$']
ylabels=['$V (V)$','tiempo (ms)','$V (V)$']

for i in range(0,3):
    axs[i].plot(ln,valores[0][i],ls='',marker='o',c='k')
    axs[i].set_title(labels[i])
    axs[i].set(ylabel=ylabels[i])
for ax in axs.flat:
    ax.set(xlabel='Ln')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()
