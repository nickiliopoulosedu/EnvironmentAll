#include "Adafruit_CCS811.h"
#include <Stepper.h>

#define SensorPin A0            //pH meter Analog output to Arduino Analog Input 0
#define Offset 0.00            //deviation compensate

#define BRAKE 0
#define CW    1
#define CCW   2
#define TR    3
#define TL    4
#define CS_THRESHOLD 15

//MOTOR 1
#define MOTOR_A1_PIN 7
#define MOTOR_B1_PIN 8

//MOTOR 2
#define MOTOR_A2_PIN 6
#define MOTOR_B2_PIN 12

#define PWM_MOTOR_1 11
#define PWM_MOTOR_2 9

#define CURRENT_SEN_1 A2
#define CURRENT_SEN_2 A3

#define EN_PIN_1 A1
#define EN_PIN_2 A2

#define MOTOR_1 0
#define MOTOR_2 1

short usSpeed = 30;
unsigned short usMotor_Status = BRAKE;

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

Stepper myStepper = Stepper(stepsPerRevolution, 2, 4, 3, 5);
Adafruit_CCS811 ccs;

void setup()
{
  pinMode(MOTOR_A1_PIN, OUTPUT);
  pinMode(MOTOR_B1_PIN, OUTPUT);

  pinMode(MOTOR_A2_PIN, OUTPUT);
  pinMode(MOTOR_B2_PIN, OUTPUT);

  pinMode(PWM_MOTOR_1, OUTPUT);
  pinMode(PWM_MOTOR_2, OUTPUT);

  pinMode(CURRENT_SEN_1, OUTPUT);
  pinMode(CURRENT_SEN_2, OUTPUT);

  pinMode(EN_PIN_1, OUTPUT);
  pinMode(EN_PIN_2, OUTPUT);

  myStepper.setSpeed(8500);

  float temp = ccs.calculateTemperature();
  ccs.setTempOffset(temp - 25);

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

  if (x > y)
  {
    dPr = y / r;
    dPm = x / mPr;
    moveForD(y, CW);
    moveForD(200, CCW);
    moveForD(0 , TR);
  }

  moveScanSend();
}
void moveScanSend()
{
  bool RL = 0;
  for (int i = 0; i <= r; i++)
  {
    for (int j = 0; <= mPr; j++)
    {
      scanAndSend();
      moveForD(dPm, CW);
    }
    moveForD(200, CCW);
    if (RL == 0)
    {
      moveForD(0, TR);
      moveForD(dPr, CW);
      moveForD(0, TR);
      moveForD(200, CCW);
      RL = 1 ;
    }
    else
    {
      moveForD(200, TL);
      moveForD(dPr, CW);
      moveForD(200, TL);
      moveForD(200, CCW);
      RL = 0;
    }
  }
  if (RL == 0)
  {
    moveForD(0, TR);
    moveForD(max(x,y), CW);
    moveForD(0, TR);
    moveForD(min(x,y), CW);
    moveForD(0, TR);
  }
}

int scanAndSend()
{
  float TEMP = ccs.calculateTemperature();
  float CO2 = ccs.geteCO2();
  float TVOC = ccs.getTVOC();
  myStepper.step(stepsPerRevolution);
  delay(2000);
  voltage = analogRead(SensorPin) * 5.0 / 1024;
  pHValue = 3.5 * voltage + Offset;
  myStepper.step(-stepsPerRevolution);
  TEMP = ccs.calculateTemperature();
  CO2 = ccs.geteCO2();
  TVOC = ccs.getTVOC();
  return TEMP, CO2, TVOC, pHValue;
}

void moveForD(int d, uint8_t direct)
{
  if (direct == 0) {}
  else if (direct == 1)
  {
    FORWARD();
    delay((((d / 100) / maxSpeed) * 1000) + 7500);
  }
  else if (direct == 2)
  {
    REVERSE();
    delay((((d / 100) / maxSpeed) * 1000) + 7500);
  }
  else if (direct == 3)
  {
    TURN_RIGHT();
    delay(delayToTurn);
  }
  else if (direct == 4)
  {
    TURN_LEFT();
    delay(delayToTurn);
  }

  STOP();
  delay(500);
}

void STOP()
{
  usMotor_Status = BRAKE;
  motorGo(MOTOR_1, usMotor_Status, 0);
  motorGo(MOTOR_2, usMotor_Status, 0);
}

void FORWARD()
{
  usMotor_Status = CW;
  motorGo(MOTOR_1, usMotor_Status, usSpeed);
  motorGo(MOTOR_2, usMotor_Status, usSpeed);
}

void REVERSE()
{
  usMotor_Status = CCW;
  motorGo(MOTOR_1, usMotor_Status, usSpeed);
  motorGo(MOTOR_2, usMotor_Status, usSpeed);
}

void TURN_LEFT()
{
  usMotor_Status = CW;
  motorGo(MOTOR_1, usMotor_Status, usSpeed);
  usMotor_Status = CCW;
  motorGo(MOTOR_2, usMotor_Status, usSpeed);
}

void TURN_RIGHT()
{
  usMotor_Status = CCW;
  motorGo(MOTOR_1, usMotor_Status, usSpeed);
  usMotor_Status = CW;
  motorGo(MOTOR_2, usMotor_Status, usSpeed);
}

void motorGo(uint8_t motor, uint8_t direct, uint8_t pwm)
{
  if (motor == MOTOR_1)
  {
    if (direct == CW)
    {
      digitalWrite(MOTOR_A1_PIN, LOW);
      digitalWrite(MOTOR_B1_PIN, HIGH);
    }
    else if (direct == CCW)
    {
      digitalWrite(MOTOR_A1_PIN, HIGH);
      digitalWrite(MOTOR_B1_PIN, LOW);
    }
    else
    {
      digitalWrite(MOTOR_A1_PIN, LOW);
      digitalWrite(MOTOR_B1_PIN, LOW);
    }
  }
  else if (motor == MOTOR_2)
  {
    if (direct == CW)
    {
      digitalWrite(MOTOR_A2_PIN, LOW);
      digitalWrite(MOTOR_B2_PIN, HIGH);
    }
    else if (direct == CCW)
    {
      digitalWrite(MOTOR_A2_PIN, HIGH);
      digitalWrite(MOTOR_B2_PIN, LOW);
    }
    else
    {
      digitalWrite(MOTOR_A2_PIN, LOW);
      digitalWrite(MOTOR_B2_PIN, LOW);
    }
  }
}

void loop() {}
