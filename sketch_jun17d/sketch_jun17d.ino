#include <SPI.h>
#include <RF24.h>

RF24 radio(9, 10); // (CE, CSN)

const byte address[6] = "5RF24";
void setup() {
  radio.begin();
  radio.setPALevel(RF24_PA_MAX); 
  radio.setChannel(125);
  radio.openReadingPipe(0, address); 
  radio.startListening();
  Serial.begin(9600);
  radio.enableDynamicPayloads();
  radio.setDataRate(RF24_250KBPS);
}

void loop() { 
  if (radio.available()) {
    byte gpsData;
    radio.read(&gpsData, sizeof(gpsData));
    Serial.write(gpsData);
  }
}
