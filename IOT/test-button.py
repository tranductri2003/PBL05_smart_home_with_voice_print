import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 14 là chân được kết nối với nút bấm

i = 0
try:
    while True:
        if GPIO.input(14) == GPIO.LOW: # Nếu nút bấm được nhấn
            print("lồn", i)
            i+=1
except KeyboardInterrupt:
    pass
