"Gets output from Plantronics Hub API and sends it to Home Assistant"
from plantronics import Spokes
from homeassistant import Sensor
from requests import post

from pathlib import Path
from winservice import SMWinservice

import time
import logging


class PlantronicsService(SMWinservice):
    _svc_name_ = "HomeAssistantPlantronicsSync"
    _svc_display_name_ = "Home Assistant Plantronics Sync"
    _svc_description_ = "Syncs Plantronics state to Home Assistant"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        self.spo = Spokes()
        self.sen = Sensor()
        self.lastState = self.spo.get_callmanager_state()["Result"]["HasActiveCall"]

        while self.isrunning:
            self.newState = self.spo.get_callmanager_state()["Result"]["HasActiveCall"]
            logging.debug(
                (
                    "Comparing last activate call state:"
                    + str(self.lastState)
                    + "with new call state:"
                    + str(self.newState)
                )
            )

            if self.lastState != self.newState:
                logging.debug(
                    (
                        "Updating Home Assistant API with new call state:"
                        + str(self.newState)
                    )
                )

                if self.newState is True:
                    self.sen.set_sensor("on")
                elif self.newState is False:
                    self.sen.set_sensor("off")
                else:
                    raise AssertionError("State should be either True or False")

            self.lastState = self.newState
            time.sleep(0.5)


if __name__ == "__main__":
    PlantronicsService.parse_command_line()
