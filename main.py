"Gets output from Plantronics Hub API and sends it to Home Assistant"
from plantronics import Spokes
from homeassistant import Sensor
from requests import post

import time
import logging

spo = Spokes()
sen = Sensor()
lastState = spo.get_callmanager_state()["Result"]["HasActiveCall"]

# Continuously check Plantronics Call Manager State
while True:
    newState = spo.get_callmanager_state()["Result"]["HasActiveCall"]
    logging.debug(
        (
            "Comparing last activate call state:"
            + str(lastState)
            + "with new call state:"
            + str(newState)
        )
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
