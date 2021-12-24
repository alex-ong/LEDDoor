from webcam_monitor.status import check_status
import time
import subprocess
from enum import Enum
import os

class LightCommand(Enum):
    ON = 1
    OFF = 2
    RED = 3
    BLUE = 4
    GREEN = 5
    PURPLE = 6

LIGHT_IP = "192.168.1.114"
BASE_CMD = f"python -m flux_led.fluxled {LIGHT_IP}"
ON_CMD = f"{BASE_CMD} -1"
OFF_CMD = f"{BASE_CMD} -0"
RED_CMD = f"{BASE_CMD} -c Red"
BLUE_CMD = f"{BASE_CMD} -c Blue"
GREEN_CMD = f"{BASE_CMD} -c Green"
PURPLE_CMD = f"{BASE_CMD} -c Purple"

CommandMap = {LightCommand.ON: ON_CMD,
              LightCommand.OFF: OFF_CMD,
              LightCommand.RED: RED_CMD,
              LightCommand.BLUE: BLUE_CMD,
              LightCommand.GREEN: GREEN_CMD,
              LightCommand.PURPLE: PURPLE_CMD}

def get_led_library_cwd():
    return os.path.abspath("flux_led")

def run_led_command(command):
    string_cmd = CommandMap[command]
    run_subprocess(string_cmd)
    
def run_subprocess(command):
    cwd = get_led_library_cwd()
    subprocess.run(command.split(), cwd=cwd)

def handle_new_status(status):
    print (status)

def main():
    last_command_ts = time.time()
    last_status = None
    while True:
        new_status = check_status()
        if new_status != last_status:
            handle_new_status(new_status)
            last_status = new_status
        time.sleep(0.5)

if __name__ == '__main__':
    t = time.time()
    for i in range (3,7):    
        run_led_command(LightCommand(i))
        print(time.time() - t)
        t = time.time()

    run_led_command(LightCommand.OFF)
