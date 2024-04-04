#include <Servo.h> // Include the Servo library to control the servo motor

Servo door1;      // Create a servo object to control the first door
Servo door2;      // Create a servo object to control the second door
int door1Pin = 3; // Specify the pin that the first servo is attached to
int door2Pin = 9; // Specify the pin that the second servo is attached to

void setup()
{
    door1.attach(door1Pin);                                    // Attach the first servo on door1Pin to the servo object
    door2.attach(door2Pin);                                    // Attach the second servo on door2Pin to the servo object
    Serial.begin(9600);                                        // Start serial communication at 9600 bits per second
    Serial.println("Setup complete. Waiting for commands..."); // Print setup complete message                            // Set pin 13 to HIGH
}

void loop()
{
    if (Serial.available() > 0)
    {                                                  // Check if there is any serial input
        String command = Serial.readStringUntil('\n'); // Read the command until newline character

        // Convert the command to uppercase to make it case-insensitive
        command.toUpperCase();

        // Use if statements to handle the commands
        if (command.equals("OPEN1"))
        {                                    // If the command is "OPEN1", open the first door
            door1.write(0);                  // Set servo to 0 degrees
            Serial.println("Door 1 OPEN");   // Print the action to Serial Monitor
            delay(3000);                     // Wait for 3 seconds
            door1.write(135);                // Set servo to 90 degrees (close position)
            Serial.println("Door 1 CLOSED"); // Print the action to Serial Monitor
        }
        else if (command.equals("OPEN2"))
        {                                    // If the command is "OPEN2", open the second door
            door2.write(0);                  // Set servo to 0 degrees
            Serial.println("Door 2 OPEN");   // Print the action to Serial Monitor
            delay(3000);                     // Wait for 3 seconds
            door2.write(135);                // Set servo to 90 degrees (close position)
            Serial.println("Door 2 CLOSED"); // Print the action to Serial Monitor
        }
        else
        { // Handle any other input as an invalid command and close the door
            Serial.println("Invalid command.");
        }
    }
}

// #include <Servo.h>      // Include the Servo library to control the servo motor
//
// Servo myservo;          // Create a servo object to control a servo
// int servoPin = 3;       // Specify the pin that the servo is attached to
//
// void setup() {
//   myservo.attach(servoPin); // Attach the servo on the servoPin to the servo object
//   Serial.begin(9600); // Start serial communication at 9600 bits per second
//   Serial.println("Setup complete. Waiting for commands..."); // Print setup complete message
// }
//
// void loop() {
//   if (Serial.available() > 0) { // Check if there is any serial input
//     String command = Serial.readStringUntil('\n'); // Read the command until newline character
//
//     // Convert the command to integer
//     int angle = command.toInt();
//
//     // Use if statements to handle the commands
//     if (angle >= 0 && angle <= 180) { // If the angle is within valid range
//       myservo.write(angle); // Set servo to the specified angle
//       Serial.print("Servo set to ");
//       Serial.print(angle);
//       Serial.println(" degrees"); // Print the action to Serial Monitor
//     } else { // Handle invalid input
//       Serial.println("Invalid angle. Please enter an angle between 0 and 180 degrees.");
//     }
//   }
// }