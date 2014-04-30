void setup() {
  // put your setup code here, to run once:

#define LD1 4
#define LD2 3
#define LD3 2
#define delay_ms 1000
#define shutter_disable 1

pinMode(LD1,OUTPUT);
pinMode(LD2,OUTPUT);
pinMode(LD3,OUTPUT);

Serial.begin(115200);

Serial.println("Arduino Laser Diode Controller Initialized!");

  if(shutter_disable == 1)
  {
    digitalWrite(LD1, HIGH);
    digitalWrite(LD2, HIGH);
    digitalWrite(LD3, HIGH);
  }
  
}

void loop() {
  

  
  int LD1val, LD2val, LD3val; // Variables to store modulation values
  
  boolean newCommand = false;  // Set the newCommand flag to false
  
  while(Serial.available() > 0) // If there is information at the serial port, excecute the following
  {
    LD1val = Serial.parseInt();  // Parse the serial input for the first integer.
    LD2val = Serial.parseInt();  // Continue and parse the serial input for the second integer.
    LD3val = Serial.parseInt();  // Continue and parse the serial input for the third integer.
    
    newCommand = true;  // Set the newCommand flag to true in order to execute the function to set the values.
  }
  
  if(newCommand && shutter_disable!=0)
  {
    if(LD1val > 1 | LD2val > 1 |LD3val > 1)
    {
      LD1val=1;
      LD2val=1;
      LD3val=1;
    }
    
    if(LD1val==1)
    {
    digitalWrite(LD1, HIGH);
    Serial.println("780 nm");
    }
    else
    {
      digitalWrite(LD1, LOW);
    }
    if(LD2val==1)
    {
    digitalWrite(LD2, HIGH);
    Serial.println("830 nm");
    }
    else
    {
      digitalWrite(LD2, LOW);
    }
    if(LD3val==1)
    {
    digitalWrite(LD3, HIGH);
    Serial.println("850 nm");
    }
    else
    {
      digitalWrite(LD3, LOW);
    }
  }
}
