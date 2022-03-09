
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

Serial.println("Inicio");
for (int medidas = 0; medidas <= n; medidas++){ //Medimos n veces la señal de cada memoria
  
//Recorremos todas las memorias FILA tras FILA
for (int k = 0; k <= 1; k++){
for (int j = 0; j <= 3; j++){ 
for (int i = 0; i <= 3; i++){ 

selector(i,j,k); //Elegimos que memoria escribimos

Serial.print(analogRead(A0));
Serial.print(',');
delay(t_read);
  
}
Serial.print('\n');
}
}

Serial.println("Final");
delay(t_read);


}

}
