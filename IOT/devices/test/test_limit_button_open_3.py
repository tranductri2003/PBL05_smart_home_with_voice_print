import RPi.GPIO as GPIO
import time

# Pin assignment
switch_pin_open = 3

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin_open, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main():
    try:
        while True:
            switch_state = GPIO.input(switch_pin_open)
            if switch_state == GPIO.LOW:
                print("Công tắc hành trình đã được kích hoạt")
            else:
                print("Công tắc hành trình không được kích hoạt")
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
