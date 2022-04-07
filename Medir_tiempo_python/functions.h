
void selector(int col, int row, int sel) {

//Encendemos el 1º Led o el 2º en función del 1º y 2º bite de col
digitalWrite(col_0,bitRead(col,0));
digitalWrite(col_1,bitRead(col,1));

//Igual con row
digitalWrite(row_0,bitRead(row,0));
digitalWrite(row_1,bitRead(row,1));

//Serial.print(sel);
digitalWrite(sel_pin, sel);

}

void reader(int n, int t_read){

for (int medidas = 0; medidas <= n; medidas++){ //Medimos n veces la señal de cada memoriaSerial.println("Inicio");
  
//Recorremos todas las memorias FILA tras FILA
for (int k = 0; k <= 1; k++){
for (int j = 0; j <= 3; j++){ 
for (int i = 0; i <= 3; i++){
   

selector(i,j,k); //Elegimos que memoria escribimos
if (medidas==1) {
digitalWrite(wrt,LOW); //Dejamos que la memoria se descargue en la primera medida
}

index=i+(j*4)+(k*16);

values[index]=analogRead(A0);   //valores de la memoria i j k convirtiendo a un valor decimal
//elapsedTime= millis() - startTime; //Tiempo en el que medimos el valor de la memoria
//times[index]=elapsedTime;

}
}
}


//Escribimos los valores de la matriz de voltaje y tiempo
for (int k = 0; k <= 1; k++){
for (int j = 0; j <= 3; j++){ 
for (int i = 0; i <= 3; i++){
index=i+(j*4)+(k*16);
Serial.println((String)values[index]);

}
}
}

Serial.println("Final");

delay(t_read);

}

}
