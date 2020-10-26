from requests import get

import json
import logging


class PLTDevice:
    def __init__(self, spokes, uid):
        self.host = "127.0.0.1"
        self.port = "32017"
        self.BaseURL = "http://" + self.host + ":" + self.port
        self.AttachURL = self.BaseURL + "/Spokes/DeviceServices/Attach?uid=" + uid
        self.attached = False
        self.session = None
        self.uid = uid
        self.spokes = spokes

    def attach(self):
        r = get(self.AttachURL)

        if r.status_code == 200:
            logging.debug(r.text)
            if r.json()["isError"] is False:
                self.attached = True
                self.session = r.json()["Result"]
        else:
            raise AssertionError(
                "Response should have status code 200, but was:", r.status
            )

    def release(self):
        self.ReleaseURL = (
            self.spokes.BaseURL + "/Spokes/DeviceServices/Release?sess=" + self.session
        )

        r = get(self.ReleaseURL)

        if r.status_code == 200:
            if r.json()["isError"] is False:
                self.attached = False
                self.session = None
        else:
            raise AssertionError(
                "Response should have status code 200, but was:", r.status
            )

    def get_events(self, queue=0):
        self.EventsURL = (
            self.spokes.BaseURL
            + "/Spokes/DeviceServices/Events?sess="
            + self.session
            + "&queue="
            + str(queue)
        )

        r = get(self.EventsURL)
        if r.status_code == 200:
            logging.debug(r.json())
        else:
            raise AssertionError(
                "Response should have status code 200, but was:", r.status
            )


class Spokes:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "32017"
        self.BaseURL = "http://" + self.host + ":" + self.port
        self.DeviceInfoURL = self.BaseURL + "/Spokes/DeviceServices/Info"
        self.CallManagerURL = self.BaseURL + "/Spokes/CallServices/CallManagerState"
        self.deviceInfo = None
        self.callManagerInfo = None

    def get_device_info(self):
        r = get(self.DeviceInfoURL)
        if r.status_code == 200:
            if r.json()["isError"] is True:
                logging.debug(r.json()["Err"]["Description"])
            else:
                self.deviceInfo = r.json()
            return self.deviceInfo
        else:
            raise AssertionError(
                "Response should have status code 200, but was:", r.status
            )

    def get_callmanager_state(self):
        r = get(self.CallManagerURL)
        if r.status_code == 200:
            if r.json()["isError"] is True:
                logging.debug(r.json()["Err"]["Description"])
            else:
                self.callManagerInfo = r.json()
            return self.callManagerInfo
        else:
            raise AssertionError(
                "Response should have status code 200, but was:", r.status
            )
