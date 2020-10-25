from plantronics import Spokes
from homeassistant import Sensor
from requests import post

import time
import logging

s = Spokes()
sen = Sensor()
lastState = s.get_callmanager_state()["Result"]["HasActiveCall"]

# Continuously check Plantronics Call Manager State
while True:
    newState = s.get_callmanager_state()["Result"]["HasActiveCall"]
    logging.debug(
        "Comparing last activate call state:",
        lastState,
        "with new call state:",
        newState,
    )

    if lastState != newState:
        print("Updating Home Assistant API with new call state:", newState)

        if newState is True:
            sen.set_sensor("on")
        elif newState is False:
            sen.set_sensor("off")
        else:
            raise AssertionError("State should be either True or False")

    lastState = newState
    time.sleep(0.5)
