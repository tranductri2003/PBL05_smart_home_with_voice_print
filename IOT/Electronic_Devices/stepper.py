import RPi.GPIO as GPIO
import time

class StepperController:
    def __init__(self, pin1, pin2, pin3, pin4, steps_per_revolution=1024, delay=0.001):
        self.StepPins = [pin1, pin2, pin3, pin4]
        self.stepsPerRevolution = steps_per_revolution
        self.delay = delay
        self.Seq = [[1, 0, 0, 1],
                    [1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 1],
                    [0, 0, 0, 1]]

        GPIO.setmode(GPIO.BCM)
        for pin in self.StepPins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def step(self, stepper, steps):
        for _ in range(steps):
            for pin in range(4):
                GPIO.output(self.StepPins[pin], stepper[pin])
            time.sleep(self.delay)

    def rotate(self, direction, revolutions):
        total_steps = self.stepsPerRevolution * revolutions
        if direction == "forward":
            for i in range(total_steps):
                self.step(self.Seq[i % 8], 1)
        elif direction == "backward":
            for i in range(total_steps - 1, -1, -1):
                self.step(self.Seq[i % 8], 1)

    def cleanup(self):
        GPIO.cleanup()

# Sử dụng lớp StepperController
if __name__ == "__main__":
    pin1 = 21  # Chân GPIO tương ứng với In1
    pin2 = 20  # Chân GPIO tương ứng với In2
    pin3 = 16  # Chân GPIO tương ứng với In3
    pin4 = 12  # Chân GPIO tương ứng với In4
    
    stepper = StepperController(pin1, pin2, pin3, pin4)

    while True:
        user_input = input("Enter 'open' to rotate forward, 'close' to rotate backward: ")
        if user_input == "open":
            stepper.rotate("forward", 6)
        elif user_input == "close":
            stepper.rotate("backward", 6)
        else:
            print("Invalid input!")

    stepper.cleanup()
