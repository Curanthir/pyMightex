void setup() {
  // put your setup code here, to run once:

#define LD1 4
#define LD2 3
#define LD3 2
#define delay_ms 500
pinMode(LD1,OUTPUT);
pinMode(LD2,OUTPUT);
pinMode(LD3,OUTPUT);

}

void loop() {
digitalWrite(LD1,HIGH);
delay(delay_ms);
digitalWrite(LD1,LOW);
digitalWrite(LD2,HIGH);
delay(delay_ms);
digitalWrite(LD2,LOW);
digitalWrite(LD3,HIGH);
delay(delay_ms);
digitalWrite(LD3,LOW);
  
}
