import Adafruit_DHT
import time

DHT_PIN = 4  # Mã GPIO của chân GPIO4

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT_PIN)
        if humidity is not None and temperature is not None:
            print(f'Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%')
        else:
            print('Failed to retrieve data from sensor. Check your connections.')

except KeyboardInterrupt:
    print('\nProgram terminated by user.')
