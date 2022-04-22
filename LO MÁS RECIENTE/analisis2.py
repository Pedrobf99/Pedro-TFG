# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 00:04:34 2022

@author: Admin
"""
import matplotlib.pylab as plt
import time
import pandas as pd
#import scipy.optimize as so
#import numpy as np
import regresion as r

folder="Datos/"
graf="graficas/"
ajust="Ajustes/"
filename="Datos_casita_python6_NCAP_sinluz.csv"

dts=[]
times=[]

# CARACTERISTICAS MEMORIAS
caract=[[4,2,1,0.5],[4,2,1,6],[2,1,0.5,4],[0.5,1,2,4],
        [66.32,100.8,206,35.6],[66.32,100.8,206,35.6],[0.5,1,2,4],[4,2,1,6]]
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

#matriz donde almacenaremos todos los datos ordenados
valores=[]
#Matrices auxiliares para recoger los datos
Vin=[]
sVin=[]
a=[]
sa=[]
Vhold=[]
sVhold=[]

bounds=[]
for j in range(0,8):
    Vin=[]
    sVin=[]
    a=[]
    sa=[]
    Vhold=[]
    sVhold=[]
    for i in range(0,4):
        #Ajustamos cada memoria a una exponencial decreciente
        coefs,scoef=r.ajuste(t_final[i+j*4][1:], b[i+j*4][1:], bounds,i+j*4)
        
        #Recogemos los valores obtenidos
        Vin.append(coefs[0])
        a.append(coefs[1])
        Vhold.append(coefs[2])
        
        sVin.append(scoef[0])
        sa.append(scoef[1])
        sVhold.append(scoef[2])
    
    valores.append([Vin,sVin,a,sa,Vhold,sVhold])

#comparamos las caract de las memorias con los valores obtenidos del ajuste
regres=r.regs(caract,valores)    
#Esta función nos da las rectas del ajuste anterior para representarlas
plots=r.plotss(caract,regres,var)


### GRAFICAR ###



for g in range(0,10):
    fig, axs = plt.subplots(1, 3)
    labels=['$V_{in}$','RC','$V_{hold}$']
    ylabels=['$V (V)$','tiempo (ms)','$V (V)$']
    
    colores=['g','b','k','gray','r','gold','lime','violet']
    mini=g/10
    for j in range(0,3):
        
        axs[j].set(ylabel=ylabels[j])
        axs[j].set_title(labels[j],loc='left')
        
        h=0
        k=[]
        for i in range(0,8):
            if var[i]!='mim':
                if h==0:
                    axs[j].set(xlabel='Ln, Lp, Wn, Wp')
                    h=1
                axs[j].errorbar(caract[i],valores[i][j*2],valores[i][j*2+1],0,
                                ls='',marker='o',c=colores[i], label=var[i], capsize=3,)
                if regres[j][4][i]>mini:
                    axs[j].plot(plots[j*8+i][0],plots[j*8+i][1], ls='--',c=colores[i])
            else:
                k.append(i)
                
        axs[j].legend(loc=0)  
        
        axs[j]=axs[j].twiny()
        for i in k:
            axs[j].errorbar(caract[i],valores[i][j*2],valores[i][j*2+1],0,
                            ls='',marker='o',c=colores[i], label=var[i], capsize=3)
            if regres[j][4][i]>mini:
                axs[j].plot(plots[j*8+i][0],plots[j*8+i][1], ls='--',c=colores[i])
            
        #axs[j].spines['bottom'].set_position(('outward',60))
        axs[j].set(xlabel='mim')
        axs[j].legend(loc=9)  
    
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    fig.set_size_inches(15, 6)
    # Wait for 1 seconds
    time.sleep(1)
    fig.savefig(ajust+filename[:-4]+'r2min'+str(mini)+'.png')
    time.sleep(1)
    plt.close(fig)

'''
tajust=input("Ver ajustes con datos experimentales ")

plt.close('all')

r.ajuste_graph(t_final, b)
'''