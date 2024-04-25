import RPi.GPIO as GPIO
import time

class MotorController:
    def __init__(self, enable_pin, in1_pin, in2_pin):
        self.enable_pin = enable_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        
        # Initialize PWM only if it has not been initialized before
        if not hasattr(self, 'pwm'):
            self.pwm = GPIO.PWM(self.enable_pin, 100)
            self.pwm.start(0)

    def forward(self, speed):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)

    def backward(self, speed):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup([self.enable_pin, self.in1_pin, self.in2_pin])

# Use case
if __name__ == "__main__":
    ENABLE_PIN = 23
    IN1_PIN = 24
    IN2_PIN = 25
    SPEED = 50  # Speed setting (0 to 100)

    # Initialize motor controller
    motor = MotorController(ENABLE_PIN, IN1_PIN, IN2_PIN)

    try:
        # Move motor forward at SPEED
        motor.forward(SPEED)
        time.sleep(2)  # Run for 2 seconds
        # Stop motor
        motor.stop()
        time.sleep(1)  # Stop for 1 second
        # Move motor backward at SPEED
        motor.backward(SPEED)
        time.sleep(2)  # Run for 2 seconds
        # Stop motor
        motor.stop()
    except KeyboardInterrupt:
        # Handle Ctrl+C interruption
        motor.stop()
    finally:
        # Cleanup GPIO when the program ends
        motor.cleanup()
