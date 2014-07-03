//Rotary Filter Array Control Program
//Jonathan Hebert with reference to Josh Brake
//7/3/2014

/*This program uses the same basic framework as the previous laser conrol programs;
however it uses a servo to control a rotating filter array. The filter is attached to the servo so that 
at 180 degrees the center filter is straight up. The filter currently rotates according to serial commands*/

// laser filter 1 is 788 nm, laser filter 2 is 830 nm, and laser filter 3 is 860 nm.
#include <Servo.h>

#define srv 5

#define LF0 180
#define LF1 121 //define positions for servo
#define LF2 94
#define LF3 68

#define LD1 4  // Define pins for laser diode outputs
#define LD2 7
#define LD3 11

Servo servo;

void setup()
{
  Serial.begin(115200);
  
  pinMode(LD1,OUTPUT);  // Configure pins as outputs
  pinMode(LD2,OUTPUT);
  pinMode(LD3,OUTPUT);
  digitalWrite(LD1, HIGH);
  digitalWrite(LD2, HIGH);
  digitalWrite(LD3, HIGH);
  
  Serial.println("Arduino Laser Diodes Activated!"); // Initialization message
  
  servo.attach(srv);
  
  servo.write(LF0);
  Serial.println("Arduino Servo Control Initialized!\n Enter 0 for no filter, 1 for 788nm, 2 for 830nm, 3 for 860nm");
  
}

void loop(){  //modified from laser diode control
  int select;
  
  boolean newCommand = false;  // Set the newCommand flag to false
  
  while(Serial.available() > 0) // If there is information at the serial port, excecute the following
  {
    select = Serial.parseInt();  // Parse the serial input.
    
    
    newCommand = true;  // Set the newCommand flag to true in order to execute the function to set the values.
  }
  
  if(newCommand){
    switch(select){
      case 0:
        servo.write(LF0);
        Serial.println("No filter selected");
        break;
      case 1:
        servo.write(LF1);
        Serial.println("788nm selected");
        break;
      case 2:
        servo.write(LF2);
        Serial.println("830nm selected");
        break;
      case 3:
        servo.write(LF3);
        Serial.println("860nm selected");
        break;
      default:
        break;  
    }
  
  }
}
