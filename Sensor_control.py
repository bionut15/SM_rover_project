import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

sensors = {
    "Front": {"TRIG": 18, "ECHO": 26},
    "Back":  {"TRIG": 22, "ECHO": 24},
    "Left":  {"TRIG": 37,  "ECHO": 21},
    "Right": {"TRIG": 13, "ECHO": 19},
}

for sensor in sensors.values():
    GPIO.setup(sensor["TRIG"], GPIO.OUT)
    GPIO.setup(sensor["ECHO"], GPIO.IN)
    GPIO.output(sensor["TRIG"], False)
time.sleep(2)

def measure_distance(trig, echo):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    start_time = time.time()
    while GPIO.input(echo) == 0:
        start_time = time.time()

    stop_time = time.time()
    while GPIO.input(echo) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return round(distance, 2)

def Sensor_control():
    try:
        while True:
            for name, pins in sensors.items():
                distance = measure_distance(pins["TRIG"], pins["ECHO"])
                print(f"{name} Sensor Distance: {distance} cm")

                # Proximity Alert
                if distance < 100:
                    print(f"⚠️ ALERT: Object detected within 1 meter at {name} side!")

            print("-" * 40)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Measurement stopped by user")
        GPIO.cleanup()
