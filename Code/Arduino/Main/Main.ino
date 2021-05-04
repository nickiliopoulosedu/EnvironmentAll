// include library for ccs811 sensor
#include "Adafruit_CCS811.h"
// include library for stepper motors
#include <Stepper.h>

// define pH meter
#define SensorPin A0                            // pH meter Analog output to Arduino Analog Input 0
#define Offset 0.00                             // deviation compensate
float voltage;
float pHValue;

// define motor functions
#define BRAKE 0
#define CW    1                                 // clockwise
#define CCW   2                                 // counterclockwise
#define TR    3                                 // turn right
#define TL    4                                 // turn left

// motor 1
#define MOTOR_A1_PIN 7                          // 7 of board to 7 of arduino
#define MOTOR_B1_PIN 8                          // 8 of board to 8 of arduino

// motor 2
#define MOTOR_A2_PIN 6                          // 4 of board to 6 of arduino
#define MOTOR_B2_PIN 12                         // 9 of board to 12 of arduino

// motor pwms
#define PWM_MOTOR_1 11                          // 5 of board to 11 of arduino 
#define PWM_MOTOR_2 9                           // 6 of board to 9 of arduino

// motor enable pins
#define EN_PIN_1 A1                             // A0 of board to A1 of arduino
#define EN_PIN_2 A2                             // A1 of board to A2 of arduino

#define MOTOR_1 0
#define MOTOR_2 1

short usSpeed = 50;                             // universal motor speed, suggested 50 or 60
const float decameters_per_second = 20;         // average speed of the robot TODO
const float delayToTurn = 1500;                 // 50 speed = 1500, 60 speed = 1050

// define field values
long x;                                         // field length
long y;                                         // field height
int rows;                                       // number of measuremennts
int scans_per_cycle;                            // measurements per row of the field
long required_field_rows;                       // required rows the field must be seperated to acheive max measurement variety
float measurement_distance;                     // distance between measurements
float field_row_distance;                       // distance between two rows of the field

// define stepper motor
Stepper myStepper = Stepper(stepsPerRevolution, 2, 4, 3, 5);
const int stepsPerRevolution = 4000;
// define ccs811 sensor
Adafruit_CCS811 ccs;

void setup()
{
  // initialise motors
  pinMode(MOTOR_A1_PIN, OUTPUT);
  pinMode(MOTOR_B1_PIN, OUTPUT);

  pinMode(MOTOR_A2_PIN, OUTPUT);
  pinMode(MOTOR_B2_PIN, OUTPUT);

  pinMode(PWM_MOTOR_1, OUTPUT);
  pinMode(PWM_MOTOR_2, OUTPUT);

  pinMode(EN_PIN_1, OUTPUT);
  pinMode(EN_PIN_2, OUTPUT);

  digitalWrite(EN_PIN_1, HIGH);
  digitalWrite(EN_PIN_2, HIGH);

  myStepper.setSpeed(5);                        // set speed of stepper motors

  Serial.begin(9600);                           // initialise serial communication

  // wait for feild length
  while (Serial.available() == 0) {}
  x = Serial.readString().toFloat();
  digitalWrite(13, HIGH);

  // wait for feild height
  while (Serial.available() == 0) {}
  y = Serial.readString().toFloat();
  digitalWrite(13, LOW);

  // wait for required number of measurements
  while (Serial.available() == 0) {}
  rows = Serial.readString().toInt();
  digitalWrite(13, HIGH);

  // wait for required measurements per row
  while (Serial.available() == 0) {}
  scans_per_cycle = Serial.readString().toInt();
  digitalWrite(13, LOW);

  // wait for required rows the field must be seperated to
  while (Serial.available() == 0) {}
  required_field_rows = Serial.readString().toInt();

  while (Serial.available() == 0) {}
  Serial.flush();

  // calculate the best way for the robot to take the most representing measurements is (rows over x or over y)
  if (x > y)
  {
    field_row_distance = x / required_field_rows; // calculate distance between field rows
    measurement_distance = y / scans_per_cycle;   // calculate distance between measurements
    // move to top left facing right
    moveForD(y, CW);
    moveForD(200, CCW);
    moveForD(0 , TR);
  }
  else
  {
    field_row_distance = y / required_field_rows; // calculate distance between field rows
    measurement_distance = x / scans_per_cycle;   // calculate distance between measurements
  }

  moveScanSend();
}
void moveScanSend()
{
  // initialise variables for measurements
  float TEMP = ccs.calculateTemperature();        // temperature variable
  float CO2 = ccs.geteCO2();                      // co2 variable
  float TVOC = ccs.getTVOC();                     // TODO variable

  bool turn_right = true;                         // bool for turning right

  // iterate for every field row
  for (int i = 0; i < required_field_rows; i++)
  {
    // iterate for every required measurement per row
    for (int j = 0; j < scans_per_cycle; j++)
    {
      moveForD(measurement_distance, CW);         // move measurement distance
      myStepper.step(stepsPerRevolution);         // insert pH meter and temperature sensor to soil

      delay(2000);                                // wait 2 seconds for accurate measurements to form

      // measure soil characteristics
      voltage = analogRead(SensorPin) * 5 / 1024; // get pH meter return voltage
      pHValue = 3.5 * voltage + Offset;           // calculate pH value
      // TODO get soil temperature

      myStepper.step(-stepsPerRevolution);        // retrack pH meter and temperature sensor

      TEMP = ccs.calculateTemperature();          // get atmospheric temperature
      CO2 = ccs.geteCO2();                        // get co2 concentration in atmosphere
      TVOC = ccs.getTVOC();                       // get TODO

      // print (transmit) values to serial monitor
      Serial.println(TEMP);
      Serial.println(CO2);
      Serial.println(TVOC);
      Serial.println(pHValue);
    }
    // test if the robot has reached the end of the field
    if (i == required_field_rows - 1 && j == scans_per_cycle - 1)
    {
      break;                                      // break from the loop
    }
    // test if the robot should turn right (it follows a sig-sag patern through the field so it sould turn once left and once right)
    if (turn_right)
    {
      // turn right
      moveForD(0, TR);                            // turn once
      moveForD(field_row_distance, CW);           // move the distance between field rows
      moveForD(0, TR);                            // turn again to correct orientation
      turn_right = false;                         // set variable to false so that next time it turns left
    }
    else
    {
      moveForD(0, TL);                            // turn once
      moveForD(field_row_distance, CW);           // move the distance between field rows
      moveForD(0, TL);                            // turn again to correct orientation
      turn_right = true;                          // set variable to true so that next time it turns right
    }
  }

  // handle the cases where the robot ends in the down right corner of the field facing down
  if (y >= x && required_field_rows % 2 == 0)
  {
    moveForD(0, TR);                              // turn right
    moveForD(x, CW);                              // go along the x axis
    moveForD(0, TR);                              // turn again to correct orientation
  }
  // handle the cases where the robot ends in the down right corner of the field facing right
  else if (x > y && required_field_rows % 2 == 1)
  {
    moveForD(y, CCW);                             // move backwards down the y axis
    moveForD(0, TL);                              // turn left to correct orientation
  }
  // handle the case where the robot ends in the top right corner of the field facing up
  else if ( y >= x && required_field_rows % 2 == 1)
  {
    moveForD(0, TL);                              // turn left
    moveForD(x, CW);                              // go along the x axis
    moveForD(0, TR);                              // turn right
    moveForD(y, CCW);                             // move backwards down the y axis
  }
  // handle the case where the robot ends in the down left corner of the field facing left
  else
  {
    moveForD(0, TR);                              // turn right to correct orientation
  }
}

// move the robot a distance
void moveForD(int d, uint8_t direct)
{
  // check if robot must move forward
  if (direct == CW)
  {
    motorGo(MOTOR_1, CW, usSpeed);                // start motor 1 clockwise
    motorGo(MOTOR_2, CW, usSpeed);                // start motor 2 clockwise
    delay((int)(d*10/decameters_per_second*1000));// wait delay defind by the formula t = d/v
  }
  
  // check if robot must move backwards
  else if (direct == CCW)
  {
    motorGo(MOTOR_1, CCW, usSpeed);               // start motor 1 counterclockwise
    motorGo(MOTOR_2, CCW, usSpeed);               // start motor 2 counterclockwise
    delay((int)(d*10/decameters_per_second*1000));// wait delay defind by the formula t = d/v
  }
  
  // check if robot must turn right
  else if (direct == TR)
  {
    motorGo(MOTOR_1, CCW, usSpeed);               // start motor 1 counterclockwise           
    motorGo(MOTOR_2, CW, usSpeed);                // start motor 2 clockwise
    delay(delayToTurn);                           // delay, fixed delay
  }

  // check if robot must turn left
  else if (direct == TL)
  {
    motorGo(MOTOR_1, CW, usSpeed);                // start motor 1 clockwise
    motorGo(MOTOR_2, CCW, usSpeed);               // start motor 2 counterclockwise
    delay(delayToTurn);                           // delay, fixed delay
  }

  motorGo(MOTOR_1, BRAKE, 0);                     // stop motor 1
  motorGo(MOTOR_2, BRAKE, 0);                     // stop motor 2
  delay(500);                                     // wait for robot to stop before begining next movement to increase accuracy of movements
}

void motorGo(uint8_t motor, uint8_t direct, uint8_t pwm)
{
  // checks if refering to motor 1
  if (motor == MOTOR_1)
  {
    // enable motor 1 clockwise
    if (direct == CW)
    {
      digitalWrite(MOTOR_A1_PIN, LOW);
      digitalWrite(MOTOR_B1_PIN, HIGH);
    }

    // enable motor 1 counterclockwise
    else if (direct == CCW)
    {
      digitalWrite(MOTOR_A1_PIN, HIGH);
      digitalWrite(MOTOR_B1_PIN, LOW);
    }

    // stop motor 1
    else
    {
      digitalWrite(MOTOR_A1_PIN, LOW);
      digitalWrite(MOTOR_B1_PIN, LOW);
    }
    // set motor 1 speed
    analogWrite(PWM_MOTOR_1, pwm);
  }

  // checks if refering to motor 2
  else if (motor == MOTOR_2)
  {
    // start motor 2 clockwise
    if (direct == CW)
    {
      digitalWrite(MOTOR_A2_PIN, LOW);
      digitalWrite(MOTOR_B2_PIN, HIGH);
    }

    // start motor 2 counterclockwise
    else if (direct == CCW)
    {
      digitalWrite(MOTOR_A2_PIN, HIGH);
      digitalWrite(MOTOR_B2_PIN, LOW);
    }

    // stop motor 2
    else
    {
      digitalWrite(MOTOR_A2_PIN, LOW);
      digitalWrite(MOTOR_B2_PIN, LOW);
    }

    // sets motor speed
    analogWrite(PWM_MOTOR_2, pwm);
  }
}

void loop() {}
