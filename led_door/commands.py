import json
from enum import Enum


def get_raw_commands():
    with open("raw_packet.json") as f:
        data = json.load(f)
    return data


RAW_COMMANDS = get_raw_commands()


class LightCommand(Enum):
    FIRE = -1
    WATER = -2
    ON = 1
    OFF = 2
    COLOR = 3


LIGHT_IP = "10.0.1.50" # doesn't support hostname
BASE_CMD = f"pipenv run python -m flux_led.fluxled {LIGHT_IP}"
ON_CMD = f"{BASE_CMD} -1"
OFF_CMD = f"{BASE_CMD} -c 0,0,0"
COLOR_CMD = f"{BASE_CMD} -c"
FIRE_CMD = f"{BASE_CMD} -r {RAW_COMMANDS['fire']}"
WATER_CMD = f"{BASE_CMD} -r {RAW_COMMANDS['water']}"

CommandMap = {
    LightCommand.ON: ON_CMD,
    LightCommand.OFF: OFF_CMD,
    LightCommand.COLOR: COLOR_CMD,
    LightCommand.FIRE: FIRE_CMD,
    LightCommand.WATER: WATER_CMD,
}


def ColorCommand(color):
    return (LightCommand.COLOR, color)
