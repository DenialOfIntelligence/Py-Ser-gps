#include <SPI.h>
#include <RF24.h>
#include <SoftwareSerial.h>
SoftwareSerial ss(4, 3);
RF24 radio(9, 10); // (CE, CSN)
const byte address[6] = "5RF24";

void setup() {
  radio.begin();
  radio.setPALevel(RF24_PA_MAX); 
  radio.setChannel(125);
  radio.openWritingPipe(address); 
  radio.stopListening();
  Serial.begin(9600);
  ss.begin(9600);
  radio.setAutoAck(true);
  radio.setRetries(5,15);
  radio.enableDynamicPayloads();
  radio.setDataRate(RF24_250KBPS);
}

void loop() {
   while (ss.available() > 0){
    byte gpsData = ss.read();
//    Serial.write(gpsData);  
    radio.write(&gpsData, sizeof(gpsData));
   }
}
