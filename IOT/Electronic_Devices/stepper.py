import RPi.GPIO as GPIO
import time

class StepperController:
    def __init__(self, pins, steps_per_revolution=1024, delay=0.001):
        self.StepPins = pins
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

# # Sử dụng lớp StepperController
# if __name__ == "__main__":
#     StepPins = [21, 20, 16, 12]  # Chân GPIO tương ứng với In1, In2, In3, In4
#     stepper = StepperController(StepPins)

#     while True:
#         user_input = input("Enter 'open' to rotate forward, 'close' to rotate backward: ")
#         if user_input == "open":
#             stepper.rotate("forward", 3)
#         elif user_input == "close":
#             stepper.rotate("backward", 3)
#         else:
#             print("Invalid input!")

#     stepper.cleanup()
