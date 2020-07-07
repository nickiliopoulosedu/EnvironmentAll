void setup()
{
  Serial.begin(9600);
  while (Serial.available() == 0)
  {
  }

  for (int i = 0; i < 100; i++)
  {
    send();
  }
}

void send()
{
  Serial.println(String(random(1, 35)));
  delay(10);
  Serial.println(String(random(1, 35)));
  delay(10);
  Serial.println(String(random(5, 75)));
  delay(100);
}

void loop()
{}
