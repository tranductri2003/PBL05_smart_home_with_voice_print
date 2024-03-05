const int motorPin1 = 12; // Chân kết nối motor
const int motorPin2 = 13; // Chân kết nối motor
int e = 11;
boolean currentOpening = false;
unsigned long startTimeOpening = 0;

void setup()
{
    pinMode(motorPin1, OUTPUT);
    pinMode(motorPin2, OUTPUT);
    pinMode(e, OUTPUT);

    Serial.begin(9600); // Khởi động giao tiếp Serial
}

void loop()
{
    if (Serial.available() > 0)
    {
        String command = Serial.readStringUntil('\n');
        if (command == "OPEN")
        {
            // Mở cửa
            digitalWrite(motorPin1, HIGH);
            digitalWrite(motorPin2, LOW);
            analogWrite(e, 50); // Tốc độ mở cửa (giả sử)
            currentOpening = true;
            startTimeOpening = millis(); // Ghi nhận thời điểm bắt đầu mở cửa
        }
    }

    if (currentOpening)
    {
        if (millis() - startTimeOpening >= 500) // Kiểm tra nếu đã mở cửa trong 0.5 giây
        {
            // Dừng cửa
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            analogWrite(e, 0);
            currentOpening = false; // Đặt lại trạng thái của cửa
        }
    }
}
