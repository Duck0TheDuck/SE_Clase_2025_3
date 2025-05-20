const int potPin = A0; // Potentiometer middle pin to A0
const int potPin1 = A1;
const int potPin2 = A2;
const int potPin3 = A3;

void setup() {
  Serial.begin(9600);  // Start serial communication
}

void loop() {
  int potValue = analogRead(potPin); 
  int potValue1 = analogRead(potPin1); 
  int potValue2 = analogRead(potPin2); 
  int potValue3 = analogRead(potPin3);
  Serial.print(potValue);
  Serial.print(",");
  Serial.print(potValue1);
  Serial.print(",");
  Serial.print(potValue2);
  Serial.print(",");
  Serial.print(potValue3);
  Serial.print(",");
  
  
  
  delay(100); // Small delay for readability
}
