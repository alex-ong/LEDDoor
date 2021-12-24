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
BASE_CMD = f"python -m flux_led.fluxled -i {LIGHT_IP}"
ON_CMD = f"{BASE_CMD} -1"
OFF_CMD = f"{BASE_CMD} -0"
LS_CMD = "ls"

def get_led_library_cwd():
    return os.path.abspath("flux_led")

def run_led_command(command):
    if command == LightCommand.ON:
        pass
    
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
    run_subprocess(ON_CMD)