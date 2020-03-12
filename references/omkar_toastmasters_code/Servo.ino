#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int angle =90;    // initial angle  for servo
int angleStep =10
;

#define LEFT 8   // pin 12 is connected to left button
#define RIGHT 7  // pin 2 is connected to right button

void setup() {
  Serial.begin(9600);          //  setup serial
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  pinMode(LEFT,INPUT_PULLUP); // assign pin 12 ass input for Left button
  pinMode(RIGHT,INPUT_PULLUP);// assing pin 2 as input for right button
  myservo.write(angle);// send servo to the middle at 90 degrees
 Serial.println("Servo Button ");
}

void loop() {
  // Servo button demo by Robojax.com
  while(digitalRead(RIGHT) == LOW){

    if (angle > 0 && angle <= 180) {
      angle = angle - angleStep;
       if(angle < 0){
        angle = 0;
       }else{
      myservo.write(angle); // move the servo to desired angle
      Serial.print("Moved to: ");
      Serial.print(angle);   // print the angle
      Serial.println(" degree");
       }
    }
    
  delay(100); // waits for the servo to get there
  }// while

  while(digitalRead(LEFT) == LOW){

    // Servo button demo by Robojax.com
    if (angle >= 0 && angle <= 180) {
      angle = angle + angleStep;
      if(angle >180){
        angle =180;
       }else{
      myservo.write(angle); // move the servo to desired angle
      Serial.print("Moved to: ");
      Serial.print(angle);   // print the angle
      Serial.println(" degree");
       }
    }
    
  delay(100); // waits for the servo to get there
  }// 

  
}
