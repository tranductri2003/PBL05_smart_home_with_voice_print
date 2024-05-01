// Видеообзоры и уроки работы с ARDUINO на YouTube-канале IOMOIO: https://www.youtube.com/channel/UCmNXABaTjX_iKH28TTJpiqA

#include "Adafruit_GFX.h"     // Библиотека обработчика графики
#include "Adafruit_ILI9341.h" // Программные драйвера для дисплеев ILI9341
#include "URTouch.h"          // Библиотека для работы с сенсорным экраном

#define TFT_DC 9              // Пин подключения вывода D/C дисплея
#define TFT_CS 10             // Пин подключения вывода CS дисплея
// Для управления очисткой экрана с помощью кнопки RESET на Arduino подключить вывод дисплея RESET через резистор к пину RESET на плате Arduino
// Для Mega 2560 вывод дисплея RESET, если не подключен в пин RESET на Arduino, подключить в 3.3V (без резистора), либо в 5V (с резистором)
#define TFT_RST 8             // Пин подключения вывода RESET (Если подключен к питанию или кнопке, то эту строку закомментировать, а следующую раскомментировать)
// #define TFT_RST -1         // Если вывод дисплея RESET подключен к питанию или через кнопку RESET на Arduino
// Uno Hardware SPI
#define TFT_MISO 12           // Пин подключения вывода дисплея SDO(MISO)
#define TFT_MOSI 11           // Пин подключения вывода дисплея SDI(MOSI)
#define TFT_CLK 13            // Пин подключения вывода дисплея SCK
/* 
//  Mega 2560 Hardware SPI
#define TFT_MOSI 51           // Пин подключения вывода дисплея SDI(MOSI)
#define TFT_CLK 52            // Пин подключения вывода дисплея SCK
#define TFT_MISO 50           // Пин подключения вывода дисплея SDO(MISO)
*/


Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_MOSI, TFT_CLK, TFT_RST, TFT_MISO);  // Создаем объект дисплея и сообщаем библиотеке распиновку для работы с графикой

#define t_SCK 3               // Пин подключения вывода дисплея T_CLK
#define t_CS 4                // Пин подключения вывода дисплея T_CS
#define t_MOSI 5              // Пин подключения вывода дисплея T_DIN
#define t_MISO 6              // Пин подключения вывода дисплея T_DOUT
#define t_IRQ 7               // Пин подключения вывода дисплея T_IRQ

URTouch ts(t_SCK, t_CS, t_MOSI, t_MISO, t_IRQ); // Создаем объект сенсорного модуля и сообщаем библиотеке распиновку для работы с ним
void setup(){
  tft.begin();                      // Initialize display
  tft.setRotation(1);               // Rotate display to landscape orientation

  tft.setTextColor(ILI9341_BLUE);  // Set text color to blue
  tft.setTextSize(1);               // Set text size to 3
  tft.setCursor(10, 50);            // Set text position
  tft.println("╒══════════════════════════════════╤══════╕");
  tft.println("│         My Smart Home            │         My Smart Home            │");
  tft.println("╞══════════════════════════════════╪══════╡");
  tft.println("│ Đèn garage                       │ Cửa cuốn garage                  │");
  tft.println("├─────────────────────────────────────────|");
  tft.println("│ Đèn garage                       │ Cửa cuốn garage                  │");
  tft.println("├─────────────────────────────────────────|");
  tft.println("│ Đèn garage                       │ Cửa cuốn garage                  │");
  tft.println("├─────────────────────────────────────────|");


}
 
void loop(){}
