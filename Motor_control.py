import RPi.GPIO as GPIO
import time
import keyboard
from adafruit_servokit import ServoKit


kit = ServoKit(channels=16)
SERVO180_CHANNEL = 1

GPIO.setmode(GPIO.BCM)
motor_pins = [8, 9, 10, 11]
pwms = []

for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)  # 50Hz PWM
    pwm.start(0)
    pwms.append(pwm)

default_angle = 90  
angle = default_angle
kit.servo[SERVO180_CHANNEL].angle = angle
time.sleep(1)

current_speed = 0

def set_all_motors(speed):
    """Set all motors to a given speed percentage (0-100)."""
    duty = 5 + (speed / 100) * 5  
    for pwm in pwms:
        pwm.ChangeDutyCycle(duty)
    print(f"Speed set to: {speed}%")

def set_angle(new_angle):
    global angle
    angle = max(0, min(180, new_angle)) 
    kit.servo[SERVO180_CHANNEL].angle = angle
    print(f"Steering angle: {angle}")
    time.sleep(0.2)

def Drive_mode_1():
    global current_speed, angle
    try:
        set_all_motors(0)
        set_angle(default_angle)
        time.sleep(2)

        while True:
            if keyboard.is_pressed('w'):
                if current_speed < 100:
                    current_speed += 5
                    set_all_motors(current_speed)
                    time.sleep(0.2)
            elif keyboard.is_pressed('s'):
                if current_speed > 0:
                    current_speed -= 5
                    set_all_motors(current_speed)
                    time.sleep(0.2)
            elif keyboard.is_pressed('d'):
                set_angle(angle + 15)
            elif keyboard.is_pressed('a'):
                set_angle(angle - 15)
            elif keyboard.is_pressed('esc'):
                print("Exiting...")
                break
    except KeyboardInterrupt:
        pass
    finally:
        set_all_motors(0)
        time.sleep(1)
        for pwm in pwms:
            pwm.stop()
        GPIO.cleanup()
        print("Motors stopped and GPIO cleaned up.")


