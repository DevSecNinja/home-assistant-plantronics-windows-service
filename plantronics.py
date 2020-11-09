from functions import get_http_result

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
        r = get_http_result(self.AttachURL)

        logging.info(r.text)
        if r.json()["isError"] is False:
            self.attached = True
            self.session = r.json()["Result"]

    def release(self):
        self.ReleaseURL = (
            self.spokes.BaseURL + "/Spokes/DeviceServices/Release?sess=" + self.session
        )
        r = get_http_result(self.ReleaseURL)

        if r.json()["isError"] is False:
            self.attached = False
            self.session = None

    def get_events(self, queue=0):
        self.EventsURL = (
            self.spokes.BaseURL
            + "/Spokes/DeviceServices/Events?sess="
            + self.session
            + "&queue="
            + str(queue)
        )
        r = get_http_result(self.EventsURL)

        logging.info(r.json())


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
        r = get_http_result(self.DeviceInfoURL)

        if r.json()["isError"] is True:
            logging.warn(r.json()["Err"]["Description"])
        else:
            self.deviceInfo = r.json()
        return self.deviceInfo

    def get_callmanager_state(self):
        r = get_http_result(self.CallManagerURL)

        if r.json()["isError"] is True:
            logging.warn(r.json()["Err"]["Description"])
        else:
            self.callManagerInfo = r.json()
        return self.callManagerInfo
