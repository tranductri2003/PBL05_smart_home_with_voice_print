#include <WiFi.h>
#include <WebServer.h>
#include "Adafruit_GFX.h"
#include "SPI.h"
#include <TFT_eSPI.h>

const char* ssid = "BIBO1-5G";
const char* password = "bibo617487";
const int serverPort = 10000;

TFT_eSPI tft = TFT_eSPI();
WebServer server(serverPort);

struct DeviceStatus {
    String name;
    int status;
};

DeviceStatus deviceStatus[] = {
    {"Garage Led", 0},
    {"Garage Door", 0},
    {"Living Led", 0},
    {"Kitchen Led", 0},
    {"Parent Led", 0},
    {"Children Led", 0}
};

String deviceTypes[] = {"led", "door", "led", "led",  "led", "led"};
double temperature = 0;
double humidity = 0;

void setup() {
  Serial.begin(115200);
  startWiFi();
  startWebServer();
  tft.begin();
  tft.setRotation(1);
  tft.fillScreen(TFT_BLACK);
  drawTable();
}

void loop() {
  server.handleClient();
}

void startWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to ");
  Serial.print(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnection established!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void startWebServer() {

  server.on("/message", HTTP_POST, []() {
    bool allArgsPresent = true;
    String missingArgs = "";

    if (server.hasArg("Garage Led")) {
      String value = server.arg("Garage Led");
      value.trim();
      deviceStatus[0].status = value.toInt();
    } else {
      allArgsPresent = false;
      missingArgs += "Garage Led, ";
    }

    if (server.hasArg("Garage Door")) {
      String value = server.arg("Garage Door");
      value.trim();
      deviceStatus[1].status = value.toInt();
    } else {
      allArgsPresent = false;
      missingArgs += "Garage Door, ";
    }

    if (server.hasArg("Living Led")) {
      String value = server.arg("Living Led");
      value.trim();
      deviceStatus[2].status = value.toInt();
    } else {
      allArgsPresent = false;
      missingArgs += "Living Led, ";
    }

    if (server.hasArg("Kitchen Led")) {
      String value = server.arg("Kitchen Led");
      value.trim();
      deviceStatus[3].status = value.toInt();
    } else {
      allArgsPresent = false;
      missingArgs += "Kitchen Led, ";
    }

    if (server.hasArg("Parent Led")) {
      String value = server.arg("Parent Led");
      value.trim();
      deviceStatus[5].status = value.toInt();
    } else {
      allArgsPresent = false;
      missingArgs += "Parent Led, ";
    }

    if (server.hasArg("Children Led")) {
      String value = server.arg("Children Led");
      value.trim();
      deviceStatus[7].status = value.toInt();
    } else {
      allArgsPresent = false;
      missingArgs += "Children Led, ";
    }

    if (server.hasArg("Temperature")) {
      String value = server.arg("Temperature");
      value.trim();
      temperature = value.toDouble();
    } else {
      allArgsPresent = false;
      missingArgs += "Temperature, ";
    }

    if (server.hasArg("Humidity")) {
      String value = server.arg("Humidity");
      value.trim();
      humidity = value.toDouble();
    } else {
      allArgsPresent = false;
      missingArgs += "Humidity, ";
    }

    if (allArgsPresent) {
      drawTable();
      server.send(200, "text/plain", "Status updated");
    } else {
      missingArgs.remove(missingArgs.length() - 2);  // Remove the last comma and space
      server.send(400, "text/plain; charset=utf-8", "Missing arguments: " + missingArgs);
    }
  });

  server.begin();
  Serial.println("HTTP server started on port " + String(serverPort));
}

void drawTable() {
  int startX = 10;
  int startY = 10;
  int cellWidth = 100;
  int cellHeight = 66;
  int tableWidth = 3 * cellWidth;
  int tableHeight = 3 * cellHeight;
  int dhtWidth = 150;
  int dhtHeight = 42;

  tft.fillRect(startX, startY, tableWidth, cellHeight, TFT_BLUE);
  tft.setTextColor(TFT_WHITE);
  tft.setTextSize(2);
  tft.setTextDatum(MC_DATUM);
  tft.drawString("MY SMART HOME", startX + tableWidth / 2, startY + cellHeight / 2);

  tft.drawRect(startX - 1, startY - 1, tableWidth + 2, tableHeight + dhtHeight + 2, TFT_BLUE);
  tft.setTextWrap(true);

  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 3; j++) {
      int index = i * 3 + j;
      int color = deviceStatus[index].status == 1 ? TFT_GREEN : TFT_RED;
      tft.drawRect(startX + j * cellWidth, startY + (i + 1) * cellHeight, cellWidth, cellHeight, TFT_BLUE);
      tft.fillRect(startX + j * cellWidth + 1, startY + (i + 1) * cellHeight + 1, cellWidth - 1, cellHeight - 1, color);
      tft.setTextColor(color == TFT_RED ? TFT_WHITE : TFT_BLACK);
      tft.setTextSize(1);
      tft.setTextDatum(TC_DATUM);
      String text = deviceStatus[index].name;
      int spaceIndex = text.indexOf(' ');
      if (spaceIndex != -1) {
        String firstWord = text.substring(0, spaceIndex);
        String secondWord = text.substring(spaceIndex + 1);
        tft.drawString(firstWord, startX + 50 + j * cellWidth, startY + 5 + (i + 1) * cellHeight);
        tft.drawString(secondWord, startX + 50 + j * cellWidth, startY + 5 + (i + 1) * cellHeight + tft.fontHeight());
      } else {
        tft.drawString(text, startX + 50 + j * cellWidth, startY + 5 + (i + 1) * cellHeight);
      }

      tft.setTextDatum(TL_DATUM);
      if (deviceTypes[index] == "door") {
        tft.fillRect(startX + 50 + j * cellWidth, startY + 40 + (i + 1) * cellHeight, 10, 15, deviceStatus[index].status == 1 ? TFT_BLUE : TFT_YELLOW);
      } else {
        tft.fillCircle(startX + 50 + j * cellWidth, startY + 45 + (i + 1) * cellHeight, 10, deviceStatus[index].status == 1 ? TFT_BLUE : TFT_YELLOW);
      }
    }
  }

  int color = temperature >= 30 ? TFT_MAGENTA : TFT_GREENYELLOW;
  tft.drawRect(startX + 0 * dhtWidth, startY + 200, dhtWidth, dhtHeight, TFT_BLUE);
  tft.fillRect(startX + 0 * dhtWidth + 1, startY + 200 + 1, dhtWidth - 1, dhtHeight - 1, color);
  tft.setTextColor(TFT_BLACK);
  tft.setTextSize(1);
  tft.drawString("Temperature: ", startX + 5 + 0 * dhtWidth, startY + 5 + 200);
  char tempStr[10];
  dtostrf(temperature, 6, 2, tempStr);
  tft.drawString(tempStr, startX + 5 + 0 * dhtWidth + tft.textWidth("Temperature: "), startY + 5 + 200);
  tft.drawString(" C", startX + 5 + 0 * dhtWidth + tft.textWidth("Temperature: ") + tft.textWidth(tempStr), startY + 5 + 200);

  color = humidity >= 60 ? TFT_CYAN : TFT_YELLOW;
  tft.drawRect(startX + 1 * dhtWidth, startY + 200, dhtWidth, dhtHeight, TFT_BLUE);
  tft.fillRect(startX + 1 * dhtWidth + 1, startY + 200 + 1, dhtWidth - 1, dhtHeight - 1, color);
  tft.setTextColor(TFT_BLACK);
  tft.setTextSize(1);
  tft.drawString("Humidity: ", startX + 5 + 1 * dhtWidth, startY + 5 + 200);
  char humStr[10];
  dtostrf(humidity, 6, 2, humStr);
  tft.drawString(humStr, startX + 5 + 1 * dhtWidth + tft.textWidth("Humidity: "), startY + 5 + 200);
  tft.drawString("%", startX + 5 + 1 * dhtWidth + tft.textWidth("Humidity: ") + tft.textWidth(humStr), startY + 5 + 200);
}
