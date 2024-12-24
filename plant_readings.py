import requests
import time
from sense_hat import SenseHat
import BlynkLib
from time import sleep
import threading

# Blynk authentication token
BLYNK_AUTH = 'GnAWG9Q0XM3vh3QFDOfTnHSi2AmyZyty'

blynk = BlynkLib.Blynk('GnAWG9Q0XM3vh3QFDOfTnHSi2AmyZyty')

# ThingSpeak channel details
THINGSPEAK_WRITE_API_KEY = '4GS7KZYMXUMMVFOW'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# Initialize SenseHat
sense = SenseHat()

# Get data from SenseHat
def get_sense_hat_data():
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    return temperature, humidity, pressure

import requests
import time
from sense_hat import SenseHat
import BlynkLib
from time import sleep
import threading

# Blynk authentication token
BLYNK_AUTH = 'GnAWG9Q0XM3vh3QFDOfTnHSi2AmyZyty'

# Initialise the Blynk instance
blynk = BlynkLib.Blynk('GnAWG9Q0XM3vh3QFDOfTnHSi2AmyZyty')

# ThingSpeak channel details
THINGSPEAK_WRITE_API_KEY = '4GS7KZYMXUMMVFOW'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# Initialize SenseHat
sense = SenseHat()

# Get data from SenseHat
def get_sense_hat_data():
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    return temperature, humidity, pressure

# Send data to ThingSpeak using requests.post method
def send_data_to_thingspeak(temperature, humidity, pressure):
    payload = {
        'api_key': THINGSPEAK_WRITE_API_KEY,
        'field1': temperature,
        'field2': humidity,
        'field3': pressure
    }
    response = requests.post(THINGSPEAK_URL, data=payload)
    if response.status_code == 200:# Send data to ThingSpeak
def send_data_to_thingspeak(temperature, humidity, pressure):
    payload = {
        'api_key': THINGSPEAK_WRITE_API_KEY,
        'field1': temperature,
        'field2': humidity,
        'field3': pressure
    }
    response = requests.post(THINGSPEAK_URL, data=payload)
 if response.status_code == 200:
        print("Data successfully sent to ThingSpeak.")
    else:
        print(f"Failed to send data to ThingSpeak. Status code: {response.status_code}")

# Blynk Virtual Pin Handlers
@blynk.on("V0")
def handle_v0_write(value):
    temperature = value[0]
    print(f'Temperature: {temperature}°C')

@blynk.on("V1")
def handle_v1_write(value):
    humidity = value[0]
    print(f'Humidity: {humidity}%')

@blynk.on("V2")
def handle_v2_write(value):
    pressure = value[0]
    print(f'Pressure: {pressure} hPa')


# Function: sends data every 30 seconds
def send_data_periodically():
    try:
        while True:
            temperature, humidity, pressure = get_sense_hat_data()
            print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Pressure: {pressure:.2f} hPa")

            # Send data to ThingSpeak
            send_data_to_thingspeak(temperature, humidity, pressure)

            # Wait for 30 seconds before taking and sending the next measurement
            time.sleep(30)
    except KeyboardInterrupt:
        print("Script terminated by user.")
# Function: allows thingspeak and blynk to work at the same time
def main():
    # Starts a thread: sends data periodically i.e. q 30seconds
    thing_speak_thread = threading.Thread(target=send_data_periodically)
    thing_speak_thread.start()

    # Loop
    print("Blynk application started. Listening for events...")
    try:
        while True:
            # Process events
            blynk.run()

            # Send data to Blynk on relevant virtual pins
            temperature = sense.get_temperature()
            blynk.virtual_write(0, temperature)  # Send temperature data to V0
            humidity = sense.get_humidity()
            blynk.virtual_write(1, humidity) # Send humidity data to V1
            pressure = sense.get_pressure()
            blynk.virtual_write(2, pressure) # Send pressure data to V2

            # Short delay
            time.sleep(1)
    except KeyboardInterrupt:
        print("Blynk application stopped.")
        thing_speak_thread.join()  # Ensure thingspeak thread finishes before main program exits

if __name__ == "__main__":
    main()
#executes main function
