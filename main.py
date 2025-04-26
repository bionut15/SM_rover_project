import subprocess
import shutil
import sys

def check_tmux_installed():
    return shutil.which("tmux") is not None

def start_tmux_four_screens(session_name="my_session", cmds=None):
    if not check_tmux_installed():
        print("Error: tmux is not installed on this system.")
        print("Please install tmux and try again.")
        sys.exit(1)

    if cmds is None or len(cmds) != 4:
        print("Error: You must provide exactly 4 commands to run.")
        sys.exit(1)

    # Start a new tmux session detached
    subprocess.run(["tmux", "new-session", "-d", "-s", session_name])

    # Split window vertically to create left and right panes
    subprocess.run(["tmux", "split-window", "-h", "-t", session_name])

    # Select the left pane and split it horizontally (top and bottom)
    subprocess.run(["tmux", "select-pane", "-t", f"{session_name}:0.0"])
    subprocess.run(["tmux", "split-window", "-v", "-t", session_name])

    # Select the right pane and split it horizontally (top and bottom)
    subprocess.run(["tmux", "select-pane", "-t", f"{session_name}:0.1"])
    subprocess.run(["tmux", "split-window", "-v", "-t", session_name])

    # Send commands to each pane
    for i, cmd in enumerate(cmds):
        subprocess.run(["tmux", "send-keys", "-t", f"{session_name}:0.{i}", cmd, "C-m"])

    # Attach to the session
    subprocess.run(["tmux", "attach-session", "-t", session_name])

if __name__ == "__main__":
    # List 4 programs you want to run
    programs = [
        "python3 Motor_control.Drive_mode_1()",        # pane 0
        "python3  Sensor_control.Sensor_control()",        # pane 1
        "python3 Camera_control.control_camera()",  # pane 2
        "python3 Gopro_library\multi_webcam\multi_webcam\examples\multiple_webcams.py"# pane 3
    ]
    start_tmux_four_screens(cmds=programs)
