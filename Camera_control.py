import time
import keyboard
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit

GPIO.setmode(GPIO.BCM)

kit = ServoKit(channels=16)

LED_PIN = 15
GPIO.setup(LED_PIN, GPIO.OUT)

ledState = False
SERVO_CHANNELS = {
    1: 0,  
    2: 1,  
    3: 2,  
    4: 3   
}
default_angle = 90
Current_camera = 1

def toggle_led():
    global ledState
    ledState = not ledState
    GPIO.output(LED_PIN, ledState)

def set_angle(channel, angle):
    kit.servo[channel].angle = angle
    time.sleep(0.2)

def move_camera(camera_num):
    if camera_num not in SERVO_CHANNELS:
        print("Invalid camera number!")
        return

    channel = SERVO_CHANNELS[camera_num]
    angle = default_angle
    set_angle(channel, angle)

    print(f"Control camera {camera_num} with W (up) and S (down), ESC to exit.")

    try:
        while True:
            if keyboard.is_pressed('w') and angle < 180:
                angle += 5
                set_angle(channel, angle)
                print(f"Moved up to {angle}°")
                time.sleep(0.2)
            elif keyboard.is_pressed('s') and angle > 0:
                angle -= 5
                set_angle(channel, angle)
                print(f"Moved down to {angle}°")
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
            print(f"\nCurrent camera: {Current_camera}")
            val = input("Enter camera number (1-4) or press Enter to move current camera: ")
            if val.isdigit():
                cam = int(val)
                if 1 <= cam <= 4:
                    Current_camera = cam
                    print(f"Switched to camera {Current_camera}")
                else:
                    print("Invalid camera number. Choose 1-4.")
            else:
                move_camera(Current_camera)

            if keyboard.is_pressed('t'):
                toggle_led()
                print(f"LED {'ON' if ledState else 'OFF'}")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")

# Run main loop
control_camera()
