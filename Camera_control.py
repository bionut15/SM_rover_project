import RPi.GPIO as GPIO
import time
import keyboard
from adafruit_servokit import ServoKit

GPIO.setmode(GPIO.BCM)
kit = ServoKit(channels=16)

# Set up servos on their respective channels
CONT_SERVO_CHANNEL = 0
SERVO180_CHANNEL = 1


Led_pin = 15

servo_pin_1 = 0
servo_pin_2 = 1
servo_pin_3 = 2
servo_pin_4 = 3

GPIO.setup(servo_pin_1, GPIO.OUT)
GPIO.setup(servo_pin_2, GPIO.OUT)
GPIO.setup(servo_pin_3, GPIO.OUT)
GPIO.setup(servo_pin_4, GPIO.OUT)
GPIO.setup(Led_pin, GPIO.OUT)

pwm_servo1 = GPIO.PWM(servo_pin_1, 50)  
pwm_servo2 = GPIO.PWM(servo_pin_2, 50)
pwm_servo3 = GPIO.PWM(servo_pin_3, 50)
pwm_servo4 = GPIO.PWM(servo_pin_4, 50)

pwm_servo1.start(0)
pwm_servo2.start(0)
pwm_servo3.start(0)
pwm_servo4.start(0)

default_angle = 180/2
Current_camera = 1

servo_pwms = {
    1: pwm_servo1,
    2: pwm_servo2,
    3: pwm_servo3,
    4: pwm_servo4
}

def set_angle( angle):
    kit.servo[SERVO180_CHANNEL].angle = angle
    time.sleep(0.5)

#Led settings (default is turned off)
ledState = False

def toggleLed():
    global ledState
    ledState = not ledState
    GPIO.output(Led_pin, ledState)

def Move_camera(Nr):
    if Nr not in servo_pwms:
        print("Invalid camera number!")
        return

    pwm_servo = servo_pwms[Nr]
    angle = default_angle
    set_angle(pwm_servo, angle)

    print(f"Control camera {Nr} with W  and S")
    
    try:
        while True:
            if keyboard.is_pressed('w'):
                if angle > 70:
                    angle += 5
                    set_angle(pwm_servo, angle)
                    print(f"Moved up to {angle} degrees")
                    time.sleep(0.2) 
            elif keyboard.is_pressed('s'):
                if angle < 70:
                    angle -= 5
                    set_angle(pwm_servo, angle)
                    print(f"Moved down to {angle} degrees")
                    time.sleep(0.2)
            elif keyboard.is_pressed('esc'):
                print("Stopping camera movement...")
                break
    except KeyboardInterrupt:
        pass

def control_camera():
    global Current_camera
    try:
        while True:
            print(f"\nCurrent camera mode: {Current_camera}")
            val = input("Change current camera (1-4), or press Enter to move current camera: ")
            if val.isdigit():
                cam = int(val)
                if 1 <= cam <= 4:
                    Current_camera = cam
                    print(f"Camera changed to {Current_camera}")
                else:
                    print("Please enter a valid camera number (1-4).")
            else:
                Move_camera(Current_camera)

            #Turn on led
            if keyboard.is_pressed('t'):
                toggleLed()
            else:
                continue
                            
    except KeyboardInterrupt:
        print("\nExiting program...")
    finally:
        pwm_servo1.stop()
        pwm_servo2.stop()
        pwm_servo3.stop()
        pwm_servo4.stop()
        GPIO.cleanup()
        print("GPIO cleaned up.")

control_camera()