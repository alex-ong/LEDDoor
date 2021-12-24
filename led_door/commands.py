import json
from enum import Enum
def get_raw_commands():
    with open("raw_packet.json") as f:
        data = json.load(f)
    return data

RAW_COMMANDS = get_raw_commands()
class LightCommand(Enum):
    ON = 1
    OFF = 2
    RED = 3
    BLUE = 4
    GREEN = 5
    PURPLE = 6
    FIRE = 7
    WATER = 8

LIGHT_IP = "192.168.1.114"
BASE_CMD = f"python -m flux_led.fluxled {LIGHT_IP}"
ON_CMD = f"{BASE_CMD} -1"
OFF_CMD = f"{BASE_CMD} -c 0,0,0"
RED_CMD = f"{BASE_CMD} -c Red"
BLUE_CMD = f"{BASE_CMD} -c Blue"
GREEN_CMD = f"{BASE_CMD} -c Green"
PURPLE_CMD = f"{BASE_CMD} -c Purple"
FIRE_CMD = f"{BASE_CMD} -r {RAW_COMMANDS['fire']}"
WATER_CMD = f"{BASE_CMD} -r {RAW_COMMANDS['water']}"

CommandMap = {LightCommand.ON: ON_CMD,
              LightCommand.OFF: OFF_CMD,
              LightCommand.RED: RED_CMD,
              LightCommand.BLUE: BLUE_CMD,
              LightCommand.GREEN: GREEN_CMD,
              LightCommand.PURPLE: PURPLE_CMD,
              LightCommand.FIRE: FIRE_CMD,
              LightCommand.WATER: WATER_CMD}