const int motorPin1 = 7;   // Chân kết nối motor
const int motorPin2 = 8;   // Chân kết nối motor
const int switchPin1 = 12; // Chân kết nối công tắc hành trình 1
const int switchPin2 = 13; // Chân kết nối công tắc hành trình 2
int e = 9;

bool isMoving = false; // Biến đánh dấu trạng thái di chuyển cửa
bool acceptedLimit1 = false;
bool forceGo = false;

unsigned long lastSwitch1Time = 0; // Biến lưu thời gian lần cuối cùng công tắc hành trình 1 được kích hoạt

void setup()
{
    pinMode(motorPin1, OUTPUT);
    pinMode(motorPin2, OUTPUT);
    pinMode(e, OUTPUT);

    pinMode(switchPin1, INPUT_PULLUP);
    pinMode(switchPin2, INPUT_PULLUP);
    //  stopMotor();
    Serial.begin(9600); // Khởi động giao tiếp Serial
}

void loop()
{
    Serial.print("CONG TAC DUNG MO: ");
    Serial.println(digitalRead(switchPin1));
    Serial.print("CONG TAC DUNG DONG: ");
    Serial.println(digitalRead(switchPin2));
    if (Serial.available() > 0)
    {
        String command = Serial.readStringUntil('\n');
        if (command == "OPEN" && !isMoving)
        {
            // Quay từ phải sang trái
            digitalWrite(motorPin1, HIGH);
            digitalWrite(motorPin2, LOW);
            analogWrite(e, 200);

            forceGo = true;
            isMoving = true;
        }
    }

    if (isMoving)
    {
        if (digitalRead(switchPin1) == LOW && acceptedLimit1 == false)
        {                               // Kiểm tra trạng thái của công tắc hành trình 1
            lastSwitch1Time = millis(); // Lưu thời gian khi công tắc hành trình 1 được kích hoạt
            // Đổi chiều quay từ trái sang phải
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            analogWrite(e, 0);
            delay(3000); // Dừng 3 giây
            Serial.println("TRUOC KHI DOI CHIEU");

            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, HIGH);
            analogWrite(e, 200);

            Serial.println("SAU KHI DOI CHIEU");
            acceptedLimit1 = true;
            forceGo = false;
        }

        if (digitalRead(switchPin2) == LOW && forceGo == false)
        { // Kiểm tra trạng thái của công tắc hành trình 2
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            analogWrite(e, 0);

            isMoving = false;
            acceptedLimit1 = false;
        }
    }
}