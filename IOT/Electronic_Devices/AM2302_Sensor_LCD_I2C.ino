#include <Wire.h> 
#include <LiquidCrystal_I2C.h> //Lib for LCD with I2C Module
#include <DHT.h> //Lib for Temperature and Humidity Sensor


LiquidCrystal_I2C lcd(0x27,16,2);
const int DHTPIN = 2; //DataPin
const int DHTTYPE = DHT22; //Use with DHT22 (AM2302)
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  lcd.init();                    
  lcd.backlight();
  dht.begin();
}

void loop() {
  float humidity, temperature;
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();

  lcd.setCursor(0,0);
  lcd.print("Temp");
  lcd.setCursor(5, 0);
  lcd.print(temperature, 1);
  lcd.setCursor(11, 0);
  lcd.print("C");

  lcd.setCursor(0,1);
  lcd.print("Humidity");
  lcd.setCursor(9, 1);
  lcd.print(humidity, 1);
  lcd.setCursor(14, 1);
  lcd.print("%");
  
  delay(1000);
  lcd.clear();
}
