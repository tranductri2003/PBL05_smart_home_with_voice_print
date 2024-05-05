#include <WiFi.h>
#include <WebServer.h>
#include "Adafruit_GFX.h"     // Graphics library
#include "SPI.h"
#include <TFT_eSPI.h> // Include the TFT_eSPI library

const char* ssid = "BIBO1-5G";
const char* password = "bibo617487";
const int serverPort = 10000; // Định nghĩa cổng của server

TFT_eSPI tft = TFT_eSPI(); 

IPAddress staticIP(192, 168, 227, 200); // Địa chỉ IP tĩnh bạn muốn gán cho thiết bị
IPAddress gateway(192, 168, 227, 1);     // Địa chỉ gateway của mạng WiFi di động
IPAddress subnet(255, 255, 255, 0);     // Subnet mask của mạng WiFi di động

WebServer server(serverPort);

String deviceStatus[][2] = {
  {"Garage Led", "OFF"},
  {"Garage Door", "OFF"},
  {"Living Door", "ON"},
  {"Living Led", "OFF"},
  {"Parent Door", "OFF"},
  {"Parent Led", "ON"},
  {"Children Door", "OFF"},
  {"Children Led", "OFF"},
  {"Kitchen Led", "OFF"},
};
String device[] = {"led", "door", "door", "led", "door", "led", "door", "led", "led"};

void setup() {
  Serial.begin(115200);
  startWiFi();
  startWebServer();
  tft.begin(); // Initialize the display
  tft.setRotation(1); // Rotate display to landscape orientation
  tft.fillScreen(TFT_BLACK);

  drawTable();
}

void loop() {
  server.handleClient();
}

void startWiFi() {
  // Thiết lập địa chỉ IP tĩnh
  //WiFi.config(staticIP, gateway, subnet);
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
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/html", "<h1>Welcome to ESP32 Web Server</h1><form action='/message' method='post'><input type='text' name='message'><input type='submit' value='Send'></form>");
  });

  server.on("/message", HTTP_POST, []() {
    String message;
    if (server.hasArg("message")) { // Kiểm tra xem tham số "message" có tồn tại không
      message = server.arg("message"); // Lấy giá trị của tham số "message"
      Serial.println(message);
      server.send(200, "text/plain; charset=utf-8", "Message received: " + message);

      int dashIndex = message.indexOf('-');
      
      // Kiểm tra xem dấu gạch ngang có tồn tại trong chuỗi hay không
      if (dashIndex != -1) {
        // Tách chuỗi thành phần thiết bị và phần trạng thái
        String device = message.substring(0, dashIndex);
        String status = message.substring(dashIndex + 2); // Bỏ qua dấu gạch ngang và khoảng trắng sau nó
      
        // Chuyển đổi thiết bị và trạng thái về dạng chữ thường
        device.trim();
        status.trim();
        
        // Cập nhật trạng thái của thiết bị
        for (int i = 0; i < sizeof(deviceStatus) / sizeof(deviceStatus[0]); i++) {
          if(device == deviceStatus[i][0]){
            deviceStatus[i][1] = status;
          }
        }
        tft.fillScreen(TFT_BLACK);
        drawTable();
      } else {
        Serial.println("Invalid message format!");
      }
    } else {
      server.send(400, "text/plain; charset=utf-8", "No message received");
    }
  });

  server.begin();
  Serial.println("HTTP server started on port " + String(serverPort));
}


void drawTable() {
  int startX = 10;
  int startY = 10; // Tăng khoảng cách từ đỉnh màn hình đến hàng tiêu đề
  int cellWidth = 100;
  int cellHeight = 60; // Tăng chiều cao ô để chứa hai dòng
  int tableWidth = 3 * cellWidth;
  int tableHeight = 4 * cellHeight; // Tăng chiều cao bảng để chứa hàng tiêu đề

  // Vẽ tiêu đề
  tft.fillRect(startX, startY, tableWidth, cellHeight, TFT_BLUE);
  tft.setTextColor(TFT_WHITE);
  tft.setTextSize(2);
  tft.setTextDatum(MC_DATUM); // Set text datum to middle-center
  tft.drawString("MY SMART HOME", startX + tableWidth/2, startY + cellHeight/2); // Draw centered text

  // Vẽ khung bảng
  tft.drawRect(startX - 1, startY - 1, tableWidth + 2, tableHeight + 2, TFT_BLUE);

  tft.setTextWrap(true); // Cho phép tự động xuống dòng khi văn bản vượt quá chiều rộng của ô

  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      int index = i * 3 + j;
      int color = TFT_RED; // Mặc định màu đỏ
      if (deviceStatus[index][1] == "ON") {
        color = TFT_GREEN; // Nếu trạng thái là ON thì màu xanh lá cây
      }

      // Vẽ viền của ô
      tft.drawRect(startX + j * cellWidth, startY + (i + 1) * cellHeight, cellWidth, cellHeight, TFT_BLUE);
      
      // Vẽ ô
      tft.fillRect(startX + j * cellWidth + 1, startY + (i + 1) * cellHeight + 1, cellWidth - 1, cellHeight - 1, color);
      
      // Vẽ chữ, chia thành hai dòng
      tft.setTextColor(color == TFT_RED ? TFT_WHITE : TFT_BLACK);
      tft.setTextSize(1);
      tft.setTextDatum(TL_DATUM); // Set text datum to top-left
      tft.drawString(deviceStatus[index][0], startX + 5 + j * cellWidth, startY + 5 + (i + 1) * cellHeight); // Draw text

      // Dịch sang dòng mới
      tft.setTextDatum(TL_DATUM); // Set text datum to top-left
      if (device[index] == "door") {
          if (deviceStatus[index][1] == "ON") {
          // Draw an open door (rectangle)
          tft.fillRect(startX + 5 + j * cellWidth, startY + 30 + (i + 1) * cellHeight, 10, 15, TFT_BLUE);
          } else {
          // Draw a closed door (rectangle)
          tft.fillRect(startX + 5 + j * cellWidth, startY + 30 + (i + 1) * cellHeight, 10, 15, TFT_YELLOW);
        }
      } else {
        // Draw a light (circle)
        if (deviceStatus[index][1] == "ON") {
          tft.fillCircle(startX + 10 + j * cellWidth, startY + 35 + (i + 1) * cellHeight, 10, TFT_BLUE);
        } else {
          tft.fillCircle(startX + 10 + j * cellWidth, startY + 35 + (i + 1) * cellHeight, 10, TFT_YELLOW);
        }
      }
      
    }
  }
}




