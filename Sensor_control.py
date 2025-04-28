import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  

sensor_pins = [24, 25, 26, 27]  

def Sensor_control():
    for pin in sensor_pins:
        GPIO.setup(pin, GPIO.IN)

    try:
        while True:
            sensor_states = []
            for pin in sensor_pins:
                state = GPIO.input(pin)
                sensor_states.append(state)
                if sensor_states.append(state) == 1:
                    print("Object detected")
                else:
                    print("Nothing detected")
            time.sleep(0.1)  

    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        GPIO.cleanup()  


