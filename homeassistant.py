import json
from plantronics import Spokes
from requests import post


class HomeAssistant:
    def __init__(self):
        with open("./secrets.json") as secrets_file:
            secrets_data = json.load(secrets_file)

        self.host = secrets_data["homeAssistantUrl"]
        self.accessToken = secrets_data["homeAssistantAccessToken"]


class Sensor(HomeAssistant):
    def __init__(self):
        s = Spokes()
        self.name = s.get_device_info()["Result"]["ProductName"]
        self.friendlyName = self.name + " Adapter"
        self.icon = "mdi:headset"

    def set_sensor(self, state):
        self.name = str(Sensor().name).replace(" ", "_")
        self.host = HomeAssistant().host + "/api/states/" + "sensor." + self.name
        self.accessToken = HomeAssistant().accessToken
        self.headers = {
            "Authorization": ("Bearer " + self.accessToken),
            "content-type": "application/json",
        }

        response = post(
            url=self.host,
            headers=self.headers,
            data=json.dumps(
                {
                    "state": state,
                    "attributes": {
                        "friendly_name": Sensor().friendlyName,
                        "icon": Sensor().icon,
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
