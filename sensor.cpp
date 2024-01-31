#include "DHT.h"

 #define DHTPIN 3

 #define DHTTYPE DHT22

 DHT dhtObject(DHTPIN, DHTTYPE);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("DHT initialized");
  dhtObject.begin();


}

void loop() {
  // put your main code here, to run repeatedly:
  float humidity = dhtObject.readHumidity();
  float Temperature = dhtObject.readTemperature();


  Serial.println("Temperature:");
  Serial.print(Temperature);
  Serial.print("degrees celcius");

  Serial.println();

  
  Serial.println("Humidity:");
  Serial.print(humidity);
  Serial.print("%");


  Serial.println();
  Serial.println();
  delay(2000);
}


// chân 1 nối nguồn
// chân 2 nối tín hiệu analog ra
// chân 4 nối đất 


//cài thư viện trong tool->manager library 
//-> tải "Adafruit DHT" và "Adafruit Unified Sensor", "DHT sensor library" của Adafruit