import RPi.GPIO as GPIO
import time
import keyboard
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
SERVO180_CHANNEL = 1

#Servo setup
servo_pin= 4
pwm_servo = GPIO.PWM(servo_pin, 50)
pwm_servo.start(0)

# depending on the servo 
default_angle=360/2

def set_angle(angle):
    kit.servo[SERVO180_CHANNEL].angle = angle
    time.sleep(0.5)

#BLDC setup
GPIO.setmode(GPIO.BCM)
motor_pins = [8, 9, 10, 11]
current_speed = 0

pwms = []

for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)  # 50Hz PWM for ESCs
    pwm.start(0)
    pwms.append(pwm)

def set_all_motors(speed):
    """Set all motors to a given speed percentage (0-100)."""
    duty = 5 + (speed / 100) * 5  # Convert to 5-10% duty cycle
    for pwm in pwms:
        pwm.ChangeDutyCycle(duty)
    print(f"Speed set to: {speed}%")

def Drive_mode_1():
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
                 if 180 <= angle <= 360:
                    angle += 15
                    set_angle(angle)
                    time.sleep(0.2)
            elif keyboard.is_pressed('a'):
                 if 0 <= angle <= 180:
                    angle -= 15
                    set_angle(angle)
                    time.sleep(0.2)
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
