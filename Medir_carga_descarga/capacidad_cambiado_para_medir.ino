/*Parte del código de Paul Badger */

#define analogPin      0          // analog pin for measuring capacitor voltage
#define chargePin      13         // pin to charge the capacitor - connected to one end of the charging resistor
#define dischargePin   11         // pin to discharge the capacitor
#define resistorValue  1000000.0F   // change this to whatever resistor value you are using

                                  // F formatter tells compliler it's a floating point value
                                  
int val[500];       //vector en el que almacenamso los datos para luego imprimirlos
int i=0;
int j=0;

unsigned long startTime;
unsigned long elapsedTime;
float microFarads;                // floating point variable to preserve precision, make calculations
float nanoFarads;

void setup(){

  pinMode(chargePin, OUTPUT);     // set chargePin to output

  digitalWrite(chargePin, LOW);

  Serial.begin(115200);             // initialize serial transmission for debugging
}

void loop(){

  digitalWrite(chargePin, HIGH);  // set chargePin HIGH and capacitor charging

  startTime = millis();

  while(analogRead(analogPin) < 1020){ // almacenamos los valores hasta que el condensador está totalmente cargado
    val[i]=analogRead(analogPin);
    i++;
  }

  elapsedTime= millis() - startTime; // tiempo que tarda en cargarse totalmente el condensador

  Serial.println("Inicio"); //empezamos a imprimir los valores del vector, señalando el inicio 
  
  for (int k = 0; k <= 499; k++){
  Serial.print(val[k]);
  Serial.print('\n');
  }

 // convert milliseconds to seconds ( 10^-3 ) and Farads to microFarads ( 10^6 ),  net 10^3 (1000)

  microFarads = ((float)elapsedTime / resistorValue) * 1000; //este valor nos da una buena aproximación de la capacidad del condensador

  /* dicharge the capacitor  */

  digitalWrite(chargePin, LOW);             // set charge pin to  LOW

  //pinMode(dischargePin, OUTPUT);            // set discharge pin to output

  //digitalWrite(dischargePin, LOW);          // set discharge pin LOW

  while(analogRead(analogPin) > 0){         // wait until capacitor is completely discharged
    val[j]=analogRead(analogPin);
    j++;
  }

  for (int k = 0; k <= j; k++){
  Serial.print(val[k]);
  Serial.print('\n');
  }

  Serial.println("Final");
  //pinMode(dischargePin, INPUT);            // set discharge pin back to input
}
