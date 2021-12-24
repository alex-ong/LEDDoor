from webcam_monitor.status import check_status
import time
import subprocess
from enum import Enum
import os

from led_door.commands import CommandMap, LightCommand

def get_led_library_cwd():
    return os.path.abspath("flux_led")

def run_led_command(command):
    string_cmd = CommandMap[command]
    run_subprocess(string_cmd)
    
def run_subprocess(command):
    cwd = get_led_library_cwd()
    subprocess.run(command.split(), cwd=cwd)

def is_in_work_meeting(items):
    return any(item in ["teams","skype","webex", "zoom"] for
               item in items)

def handle_new_status(status, last_command):
    print (status)
    webcam, mic = status
    command = LightCommand.OFF
    if len(webcam) > 0:    
        # Always run fire or water if webcam is on
        all_items = webcam+mic
        if is_in_work_meeting(all_items):
            command = LightCommand.FIRE
        else:
            command = LightCommand.WATER
    elif len(mic) > 0:
        if is_in_work_meeting(mic):        
            command = LightCommand.FIRE
        elif "discord" in mic:
            command = LightCommand.RED
        else:
            command = LightCommand.BLUE
    
    if command != last_command:
        run_led_command(command)
        
    return command
        
    

def main():
    run_led_command(LightCommand.ON)    
    last_command = None
    last_status = None
    
    while True:
        new_status = check_status()
        if new_status != last_status:
            last_command = handle_new_status(new_status, 
                                             last_command)
            last_status = new_status
        time.sleep(0.5)

if __name__ == '__main__':
    main()
