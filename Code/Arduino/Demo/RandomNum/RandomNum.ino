int x;
int y;
int rows;
int r;
int mPr;
int dPm;
int dPr;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 5; i++)
  {
    while (Serial.available() == 0) {}
    Serial.readString();
  }
    for (int i = 0; i < 100; i++)
  {
    Serial.println((String)random(35, 1500));
    Serial.println((String)random(35, 1500));
    Serial.println((String)random(35, 1500));
  }

}

void loop() {

}
