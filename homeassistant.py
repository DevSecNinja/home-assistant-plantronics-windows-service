import json
import os
import sys
import logging

from plantronics import Spokes
from requests import post


class HomeAssistant:
    def __init__(self):
        try:
            with open(os.path.join(sys.path[0], "secrets.json")) as secrets_file:
                secrets_data = json.load(secrets_file)
        except IOError:
            logging.debug(
                (
                    "The secrets.json file does not exist.",
                    "Copy secrets.example.json and rename it to secrets.json.",
                    "Make sure to edit the placeholder",
                )
            )
            raise

        self.host = secrets_data["homeAssistantUrl"]
        self.accessToken = secrets_data["homeAssistantAccessToken"]


class Sensor(HomeAssistant):
    def __init__(self):
        self.name = Spokes().get_device_info()["Result"]["ProductName"]
        self.friendlyName = self.name + " Adapter"
        self.icon = "mdi:headset"

    def set_sensor(self, state):
        sen = Sensor()

        self.name = str(sen.name).replace(" ", "_")
        self.host = HomeAssistant().host + "/api/states/" + "sensor." + self.name
        self.accessToken = HomeAssistant().accessToken
        self.headers = {
            "Authorization": ("Bearer " + self.accessToken),
            "content-type": "application/json",
        }

        try:
            response = post(
                url=self.host,
                headers=self.headers,
                data=json.dumps(
                    {
                        "state": state,
                        "attributes": {
                            "friendly_name": sen.friendlyName,
                            "icon": sen.icon,
                        },
                    }
                ),
            )

            if response.status_code == 200 or response.status_code == 201:
                self.sensorInfo = response.json
                return self.sensorInfo
            else:
                raise AssertionError(
                    "Response should have status code 200 or 201, but was:",
                    response.status_code,
                )

        except Exception as e:
            logging.critical(
                ("Failed to update Home Assistant sensor. Exception:" + str(e))
            )
