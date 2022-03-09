//Nombramos cada pin con lo que representan
int row_0=4;
int row_1=5;
int col_0=6;
int col_1=7;
int sel_pin=3;
int wrt=8;
int n=5; //Númeo de medidas


// tiempo entre escrituras /tiempo entre medidas  /matriz con los valores analógicos
int t_wrt=100;
int t_read=10;
float values[4][8]={};

//Elegimos que memoria queremos usar
int col=3; //del 0 al 3
int row=3; //del 0 al 3
int sel=1; //del 0 (seln) al 1 (sel)

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
digitalWrite(wrt,LOW);

}
}
}

//Con esta funcion leemos en orden el valor de cada memoria n veces, esperando un tiempo t_read entre cada ciclo
reader(n,t_read);

//selector(col,row,sel);

}
