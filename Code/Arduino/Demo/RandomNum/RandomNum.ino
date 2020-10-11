int x;
int y;
int rows;
int r;
int mPr;
int dPm;
int dPr;
const float maxSpeed = 0;
const float delayToTurn = 0;
const int stepsPerRevolution = 40000000000;

float voltage;
float pHValue;

void setup() {
  Serial.begin(9600);

  while (Serial.available() == 0) {}
  x = Serial.readString().toInt();

  while (Serial.available() == 0) {}
  y = Serial.readString().toInt();

  while (Serial.available() == 0) {}
  rows = Serial.readString().toInt();

  while (Serial.available() == 0) {}
  r = Serial.readString().toInt();

  while (Serial.available() == 0) {}
  mPr = Serial.readString().toInt();
  dPm = y / mPr;
  dPr = x / r;

  while (Serial.available() == 0) {}
  Serial.readString();

}

void loop() {
  for (int i = 0; i < 100; i++)
  {
    Serial.println(random(35, 1500));
    Serial.println(random(35, 1500));
    Serial.println(random(35, 1500));
  }

}
