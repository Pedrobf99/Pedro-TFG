
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
