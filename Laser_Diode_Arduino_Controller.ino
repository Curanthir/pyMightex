// Laser Diode Controller Program
// Joshua Brake
// 10/8/13

// Program Explanation:
// The program waits for an input from the command line serial interface to set the value of the intensity for the laser diodes.
// The input value should be 0 or 1 corresponding to off and on.
// Input structure should be the values separated with a delimiter such as a space or a period.
// For example, "0 0 0" will set all laser diodes off. "1 1 0" will set laser diode 1 to on, laser diode 2 to on, and laser diode 3 to off.
// In our setup, laser diode 1 is 788 nm, laser diode 2 is 808 nm, and laser diode 3 is 830 nm.

#define LD1 3  // Define pins for laser diode outputs
#define LD2 5
#define LD3 6
#define LD1PM 0
#define LD1CM 1
#define LD2PM 2
#define LD2CM 3
#define LD3PM 4
#define LD3CM 5

void setup()
{
  Serial.begin(11520);
  
  pinMode(LD1,OUTPUT);  // Configure pins as outputs
  pinMode(LD2,OUTPUT);
  pinMode(LD3,OUTPUT);
  
  Serial.println("Arduino Laser Diode Controller Initialized!"); // Initialization message
  Serial.println();
}

void loop()
{
  
  int LD1val, LD2val, LD3val; // Variables to store modulation values
  
  boolean newCommand = false;  // Set the newCommand flag to false
  
  while(Serial.available() > 0) // If there is information at the serial port, excecute the following
  {
    LD1val = Serial.parseInt();  // Parse the serial input for the first integer.
    LD2val = Serial.parseInt();  // Continue and parse the serial input for the second integer.
    LD3val = Serial.parseInt();  // Continue and parse the serial input for the third integer.
    
    newCommand = true;  // Set the newCommand flag to true in order to execute the function to set the values.
  }
  
  if(newCommand)
  {
    if(LD1val > 1 | LD2val > 1 |LD3val > 1)
    {
      LD1val=1;
      LD2val=1;
      LD3val=1;
    }
    
    if(LD1val==1)
    {
    digitalWrite(LD1, LOW); 
    }
    else
    {
      digitalWrite(LD1, HIGH);
    }
    if(LD2val==1)
    {
    digitalWrite(LD2, LOW);
    }
    else
    {
      digitalWrite(LD2, HIGH);
    }
    if(LD3val==1)
    {
    digitalWrite(LD3, LOW);
    }
    else
    {
      digitalWrite(LD3, HIGH);
    }
    
    Serial.print("Laser Diode 1 turned: ");  // Provide serial output indicating which lasers are ON and which are OFF.
    if(LD1val==1)
    {
    Serial.println("ON.");
    }
    else
    {
      Serial.println("OFF.");
    }
    
    Serial.print("Laser Diode 2 turned to: ");
    if(LD2val==1)
    {
    Serial.println("ON.");
    }
    else
    {
      Serial.println("OFF.");
    }
    
    Serial.print("Laser Diode 3 turned to: ");
    if(LD3val==1)
    {
    Serial.println("ON.");
    }
    else
    {
      Serial.println("OFF.");
    }
    
    Serial.println();
  
  delay(1000);
  
  float PM = analogRead(LD1PM);
  PM = PM * 0.0048828125;
  float CM = analogRead(LD1CM);
  CM = CM * 0.0048828125;
  Serial.print("LD1PM: ");
  Serial.print(PM);
  Serial.print(" LD1CM: ");
  Serial.println(CM);
  
  PM = analogRead(LD2PM);
  PM = PM * 0.0048828125;
  CM = analogRead(LD2CM);
  CM = CM * 0.0048828125;
  Serial.print("LD2PM: ");
  Serial.print(PM);
  Serial.print(" LD2CM: ");
  Serial.println(CM);
  
  PM = analogRead(LD3PM);
  PM = PM * 0.0048828125;
  CM = analogRead(LD3CM);
  CM = CM * 0.0048828125;
  Serial.print("LD3PM: ");
  Serial.print(PM);
  Serial.print(" LD3CM: ");
  Serial.println(CM);
  Serial.println("");
  }
}


