int val=0;
int wrt=9;
int pin=A0;

void setup() {
Serial.begin(115200);
pinMode(wrt, OUTPUT);
pinMode(pin, INPUT);
Serial.println("Inicio");
digitalWrite(wrt,HIGH);
}

void loop() {

val=analogRead(pin);
Serial.println(val);
}
