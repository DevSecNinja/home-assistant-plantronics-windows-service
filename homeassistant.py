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
            logging.error(
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
        self.spo = Spokes()
        self.name = self.spo.get_device_info()["Result"]["ProductName"]
        self.friendlyName = self.name + " Adapter"
        self.icon = "mdi:headset"

    def set_sensor(self, state):
        sen = Sensor()

        self.name = str(sen.name).replace(" ", "_")
        self.host = HomeAssistant().host + "/api/states/" + "sensor." + self.name
        self.accessToken = HomeAssistant().accessToken
        self.computerName = os.environ["COMPUTERNAME"]
        self.headers = {
            "Authorization": ("Bearer " + self.accessToken),
            "content-type": "application/json",
        }

        try:
            self.source = self.spo.get_callmanager_state()["Result"]["Calls"][0][
                "Source"
            ]
        except Exception:
            self.source = None

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
                            "source": self.source,
                            "computer_name": self.computerName,
                        },
                    }
                ),
            )
        except ConnectionError as e:
            logging.warn("Request to Home Assistant failed", e)
        finally:
            if response.status_code == 200 or response.status_code == 201:
                self.sensorInfo = response.json
                return self.sensorInfo
            else:
                logging.error(
                    "Response should have status code 200 or 201, but was:",
                    response.status_code,
                )
