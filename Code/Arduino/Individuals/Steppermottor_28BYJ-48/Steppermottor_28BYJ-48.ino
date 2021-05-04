/* Example sketch to control a 28BYJ-48 stepper motor with ULN2003 driver board and Arduino UNO. More info: https://www.makerguides.com */
// Include the Arduino Stepper.h library:
#include <Stepper.h>
// Define number of steps per rotation:
const int stepsPerRevolution = 4000;

Stepper myStepper = Stepper(stepsPerRevolution, 2, 4, 3, 5);
void setup() {
  // Set the speed to 5 rpm:
  myStepper.setSpeed(5);
  // Begin Serial communication at a baud rate of 9600:
 }
void loop() {
    //myStepper.setSpeed(motorSpeed);
    myStepper.step(stepsPerRevolution);

}
