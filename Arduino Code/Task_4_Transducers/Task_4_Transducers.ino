#include<Wire.h>
#include<SoftwareSerial.h>

const int MPU_addr=0x68;
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;

int minVal=265;
int maxVal=402;
SoftwareSerial BLE(0,1);
const int SENSOR_PIN = 11;
int lastState = LOW;      // the previous state from the input pin
int currentState;
int isTouched;
double x;
double y;
double z;

void setup(){
Wire.begin();
Wire.beginTransmission(MPU_addr);
Wire.write(0x6B);
Wire.write(0);
Wire.endTransmission(true);
Serial.begin(9600);
pinMode(SENSOR_PIN, INPUT);
BLE.begin(9600);
}

void loop(){
Wire.beginTransmission(MPU_addr);
Wire.write(0x3B);
Wire.endTransmission(false);
Wire.requestFrom(MPU_addr,14,true);
AcX=Wire.read()<<8|Wire.read();
AcY=Wire.read()<<8|Wire.read();
AcZ=Wire.read()<<8|Wire.read();

int xAng = map(AcX,minVal,maxVal,-90,90);
int yAng = map(AcY,minVal,maxVal,-90,90);
int zAng = map(AcZ,minVal,maxVal,-90,90);

x= RAD_TO_DEG * (atan2(-yAng, -zAng)+PI);
y= RAD_TO_DEG * (atan2(-xAng, -zAng)+PI);
z= RAD_TO_DEG * (atan2(-yAng, -xAng)+PI);

currentState = digitalRead(SENSOR_PIN);
if(lastState == LOW && currentState == HIGH){
  isTouched = 1;
}
else{
  isTouched = 0;
}
// save the the last state
lastState = currentState;

Serial.print(x);
Serial.print("/");
Serial.print(y);
Serial.print("/");
// Serial.print(z);
// Serial.print("/");
Serial.println(isTouched);
delay(200);
}