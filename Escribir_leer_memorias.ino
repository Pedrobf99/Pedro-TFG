//Nombramos cada pin con lo que representan
int row_0=4;
int row_1=5;
int col_0=6;
int col_1=7;
int sel_pin=3;
int wrt=8;
//int k;


// tiempo entre escrituras /tiempo entre medidas  /matriz con los valores analógicos
int t_wrt=500;
int trd=100;
float values[4][8]={};

//Elegimos que memoria queremos usar
int col=3; //del 0 al 3
int row=3; //del 0 al 3
int sel=1; //del 0 (seln) al 1 (sel)

#include "functions.h"

void setup() { 
Serial.begin(9600);
pinMode(sel_pin, OUTPUT); //sel o seln
pinMode(row_0, OUTPUT);   //primer bite de la row
pinMode(row_1, OUTPUT);   //segundo bite de la row
pinMode(col_0, OUTPUT);   //primer bite de la col
pinMode(col_1, OUTPUT);   //segundo bite de la col
pinMode(wrt, OUTPUT);     //write pin
pinMode(A0, INPUT);
}

void loop() {

//Recorremos todas las memorias
for (int i = 0; i <= 3; i++){ 
for (int j = 0; j <= 3; j++){ 
for (int k = 0; k <= 1; k++){

selector(i,j,k); //Recorremos todas las matrices

//Escribimos durante un tiempo t_wrt
digitalWrite(wrt,HIGH);
delay(t_wrt);

if (k==0) {values[j][i]=analogRead(A0);}   //valores de las memorias seln
if (k==1) {values[j][i+4]=analogRead(A0);} // valores de las memorias sel

digitalWrite(wrt,LOW);
delay(t_wrt);
}
}
}

//Escribimos la matriz explícitamente

Serial.println("Inicio");

for ( int i = 0; i < 8; i++ ){
for ( int j = 0; j < 4; j++ ){
   Serial.print(values[ j ][ i ]);
   Serial.print(',');
}
Serial.print('\n');
}

Serial.println("Final");

//selector(col,row,sel);


}
