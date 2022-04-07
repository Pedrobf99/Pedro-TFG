//Nombramos cada pin con lo que representan
int row_0=4;
int row_1=5;
int col_0=6;
int col_1=7;
int sel_pin=3;
int wrt=8;
int n=40; //Númeo de medidas
int index=0;

// tiempo entre escrituras /tiempo entre medidas  /matriz con los valores analógicos
int t_wrt=100;
int t_read=5;
float values[32]={};
float times[32]={};
unsigned long startTime;
unsigned long elapsedTime;

#include "functions.h"

void setup() { 
Serial.begin(115200); 
pinMode(sel_pin, OUTPUT); //sel o seln
pinMode(row_0, OUTPUT);   //primer bite de la row
pinMode(row_1, OUTPUT);   //segundo bite de la row
pinMode(col_0, OUTPUT);   //primer bite de la col
pinMode(col_1, OUTPUT);   //segundo bite de la col
pinMode(wrt, OUTPUT);     //write pin
pinMode(A0, INPUT);
Serial.println("Medidas");
Serial.println(n);
}

void loop() {

//Recorremos todas las memorias FILA tras FILA
for (int k = 0; k <= 1; k++){
for (int j = 0; j <= 3; j++){ 
for (int i = 0; i <= 3; i++){ 

selector(i,j,k); //Elegimos que memoria escribimos

//Escribimos 
digitalWrite(wrt,HIGH);
delay(t_wrt);

}
}
}

Serial.println("SuperInicio"); //Escribimos para saber cuando empieza el loop

startTime = millis(); //Inicio de las medidas para tener una referencia

//Con esta funcion leemos en orden el valor de cada memoria n veces, esperando un tiempo t_read entre cada ciclo
for (int medidas = 0; medidas <= n; medidas++){ //Medimos n veces la señal de cada memoria
reader(startTime,medidas,t_read);
}

}
