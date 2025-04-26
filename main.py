import Motor_control
import Camera_control
import Sensor_control


def main():
    Motor_control.Drive_mode_1()
    Camera_control.control_camera()
    Sensor_control.Sensor_control()

if __name__=="__main__":
    main()
