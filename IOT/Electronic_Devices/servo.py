import RPi.GPIO as GPIO
import time

class ServoController:
    def __init__(self, pin=23, frequency=50):
        """Initialize the GPIO pin for the servo and set PWM frequency."""
        self.pin = pin
        self.frequency = frequency
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, self.frequency)
        self.servo.start(0)

    def set_servo_angle(self, angle):
        """Move the servo to a specific angle based on the PWM duty cycle."""
        duty_cycle = (angle / 18.0) + 2  # Convert angle to PWM duty cycle
        self.servo.ChangeDutyCycle(duty_cycle)
        time.sleep(1)  # Allow the servo time to move to the position
        self.servo.ChangeDutyCycle(0)  # Stop the PWM signal

    def open_door(self, angle):
        """Open the door to the pre-defined open position (angle degrees)."""
        self.set_servo_angle(angle)

    def close_door(self, angle):
        """Close the door by returning it to the zero degree position."""
        self.set_servo_angle(angle)

    def custom_angle(self, angle):
        """Move the door to a custom angle specified by the user."""
        if 0 <= angle <= 180:
            self.set_servo_angle(angle)
        else:
            print("Error: Angle must be between 0 and 180 degrees.")

    def open_door_close_door(self, angle, time_to_wait):
        """Open and close door"""
        self.open_door(angle)  # Adjust the door to angle degrees
        time.sleep(time_to_wait)  # Keep the door open for 3 seconds
        self.close_door(110)  # Close the door to an angle of 0 degrees
        
    def cleanup(self):
        """Clean up GPIO and stop PWM when done using the controller."""
        self.servo.stop()
        GPIO.cleanup()

# # Example usage
# if __name__ == "__main__":
#     door_controller = ServoController(pin=8)
    
#     # Example of opening and closing the door
#     door_controller.open_door_close_door(0, 3)

#     # Optionally set a custom angle
#     # door_controller.custom_angle(90)  # Adjust the door to 90 degrees

#     # Cleanup GPIO and PWM
#     door_controller.cleanup()
