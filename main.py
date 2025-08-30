from enum import Enum
import time
import subprocess
import os
import logging

from PIL import Image
from pystray import Icon, Menu, MenuItem
from webcam_monitor.status import check_status
from led_door.commands import CommandMap, LightCommand, ColorCommand

logging.basicConfig(
    filename="logging.log",
    filemode="w",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_led_library_cwd():
    return os.path.abspath("flux_led")


def run_led_command(command):
    if isinstance(command, LightCommand):
        string_cmd = CommandMap[command]
    else:
        string_cmd = CommandMap[command[0]] + " " + command[1]
    run_subprocess(string_cmd)


def run_subprocess(command):
    cwd = get_led_library_cwd()
    subprocess.run(command.split(), cwd=cwd)


def is_in_work_meeting(items):
    return any(item in ["teams", "skype", "webex", "zoom"] for item in items)


def handle_new_status(status, last_command, is_force_disabled):
    webcam, mic = status
    command = LightCommand.OFF
    if is_force_disabled:
        pass
    elif len(webcam) > 0:
        # Always run fire or water if webcam is on
        all_items = webcam + mic
        if is_in_work_meeting(all_items):
            command = LightCommand.FIRE
        else:
            command = LightCommand.WATER
    elif len(mic) > 0:
        if is_in_work_meeting(mic):
            command = LightCommand.FIRE
        elif "discord" in mic:
            command = ColorCommand("69,0,255")
        elif "riotclientservices" in mic:
            command = ColorCommand("255, 37, 255")
        else:
            command = ColorCommand("Blue")

    if command != last_command:
        logging.info(f"{status}")
        run_led_command(command)

    return command


def main(icon):
    run_led_command(LightCommand.ON)
    last_sent_ts = time.time()
    last_command = None
    last_status = None
    last_force_off = is_force_off_checked()
    icon.visible = True
    while not icon._led_stop:
        new_status = check_status()
        if (
            new_status != last_status
            or time.time() - last_sent_ts > 60
            or last_force_off != is_force_off_checked()
        ):
            last_command = handle_new_status(
                new_status, last_command, is_force_off_checked()
            )
            last_status = new_status
            last_force_off = is_force_off_checked
            last_sent_ts = time.time()
        time.sleep(0.016)


class ImageEnum(Enum):
    RGBDoor = "RGBDoor.png"
    Black = "BlackDoor.png"


def create_image(image_enum: ImageEnum = ImageEnum.RGBDoor) -> Image:
    image = Image.open(image_enum.value)
    return image


def close_app(icon, _):
    icon._led_stop = True
    icon.stop()


FORCE_OFF = False


def toggle_force_off(icon, _):
    global FORCE_OFF
    FORCE_OFF = not FORCE_OFF
    if FORCE_OFF:
        icon.icon = create_image(ImageEnum.Black)
    else:
        icon.icon = create_image(ImageEnum.RGBDoor)


def is_force_off_checked(_=None):
    global FORCE_OFF
    return FORCE_OFF


def create_icon():
    icon = Icon(
        "LEDDoor",
        create_image(),
        menu=Menu(
            MenuItem("Force Disable", toggle_force_off, checked=is_force_off_checked),
            MenuItem("Close", close_app),
        ),
    )

    return icon


if __name__ == "__main__":
    icon = create_icon()
    icon._led_stop = False
    icon.run(main)
