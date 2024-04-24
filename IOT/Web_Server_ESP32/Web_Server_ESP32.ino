#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Galaxy A23 5G";
const char* password = "012345677";
const int serverPort = 10000; // Định nghĩa cổng của server

WebServer server(serverPort);

void setup() {
  Serial.begin(115200);
  startWiFi();
  startWebServer();
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
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/html", "<h1>Welcome to ESP32 Web Server</h1><form action='/message' method='post'><input type='text' name='message'><input type='submit' value='Send'></form>");
  });

  server.on("/message", HTTP_POST, []() {
    String message;
    if (server.hasArg("message")) { // Kiểm tra xem tham số "message" có tồn tại không
      message = server.arg("message"); // Lấy giá trị của tham số "message"
      Serial.println("Received message: " + message);
      Serial.println("Message received: " + message);
      server.send(200, "text/plain", "Message received: " + message);
    } else {
      server.send(400, "text/plain", "No message received");
    }
  });

  server.begin();
  Serial.println("HTTP server started on port " + String(serverPort));
}

