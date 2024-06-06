import RPi.GPIO as GPIO
import time

class MotorController:
    def __init__(self, enable_pin, motor_pin1, motor_pin2, switch_pin_open, switch_pin_close):
        self.enable_pin = enable_pin
        self.motor_pin1 = motor_pin1
        self.motor_pin2 = motor_pin2
        self.switch_pin_open = switch_pin_open
        self.switch_pin_close = switch_pin_close

        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.motor_pin1, self.motor_pin2, self.enable_pin], GPIO.OUT)
        GPIO.setup(self.switch_pin_open, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switch_pin_close, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # PWM setup
        self.pwm = GPIO.PWM(self.enable_pin, 10)  # Set PWM frequency to 1 kHz
        self.pwm.start(0)

    def stop_motor(self):
        GPIO.output([self.motor_pin1, self.motor_pin2], GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

    def open_door(self):
        # Open the door
        GPIO.output(self.motor_pin1, GPIO.HIGH)
        GPIO.output(self.motor_pin2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(20)  # Set duty cycle to 20%

    def close_door(self):
        # Close the door
        GPIO.output(self.motor_pin1, GPIO.LOW)
        GPIO.output(self.motor_pin2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(20)

    def open_door_close_door(self, time_to_wait):
        is_moving = False
        enough_time_to_wait_to_open = False
        force_open = False

        while True:
            # print("Switch Open State:", GPIO.input(self.switch_pin_open))
            # print("Switch Close State:", GPIO.input(self.switch_pin_close))

            if is_moving == False:
                self.open_door()
                force_open = True
                is_moving = True

            if is_moving == True:
                if GPIO.input(self.switch_pin_open) == GPIO.LOW and enough_time_to_wait_to_open == False:
                    self.stop_motor()
                    time.sleep(time_to_wait)
                    self.close_door()
                    enough_time_to_wait_to_open = True
                    force_open = False

                if GPIO.input(self.switch_pin_close) == GPIO.LOW and force_open == False:
                    self.stop_motor()
                    is_moving = False
                    enough_time_to_wait_to_open = False
                    break


try:
    door_controller = MotorController(enable_pin=14, motor_pin1=15, motor_pin2=18, switch_pin_open=3, switch_pin_close=24)
    door_controller.open_door_close_door(3)
except KeyboardInterrupt:
    door_controller.stop_motor()
finally:
    door_controller.stop_motor()
    GPIO.cleanup()