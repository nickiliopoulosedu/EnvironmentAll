#define SensorPin A0            //pH meter Analog output to Arduino Analog Input 0
#define Offset 0.00            //deviation compensate
float voltage;
float pHValue;
void setup(void)
{
  Serial.begin(9600);
  Serial.println("pH meter experiment!");    //Test the serial monitor
}
void loop(void)
{
  voltage = analogRead(SensorPin)*5.0/1024;
  pHValue = 3.5*voltage+Offset;
  Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.print("    pHValue: ");
  Serial.println(pHValue);
  delay(1000);
}
