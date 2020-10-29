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
        try:
            r = get(self.AttachURL)
        except ConnectionError as e:
            logging.warn("Request to local Plantronics API failed", e)
            pass

        if r.status_code == 200:
            logging.info(r.text)
            if r.json()["isError"] is False:
                self.attached = True
                self.session = r.json()["Result"]
        else:
            logging.error("Response should have status code 200, but was:", r.status)

    def release(self):
        self.ReleaseURL = (
            self.spokes.BaseURL + "/Spokes/DeviceServices/Release?sess=" + self.session
        )
        try:
            r = get(self.ReleaseURL)
        except ConnectionError as e:
            logging.warn("Request to local Plantronics API failed", e)
            pass

        if r.status_code == 200:
            if r.json()["isError"] is False:
                self.attached = False
                self.session = None
        else:
            logging.error("Response should have status code 200, but was:", r.status)

    def get_events(self, queue=0):
        self.EventsURL = (
            self.spokes.BaseURL
            + "/Spokes/DeviceServices/Events?sess="
            + self.session
            + "&queue="
            + str(queue)
        )
        try:
            r = get(self.EventsURL)
        except ConnectionError as e:
            logging.warn("Request to local Plantronics API failed", e)
            pass

        if r.status_code == 200:
            logging.info(r.json())
        else:
            logging.error("Response should have status code 200, but was:", r.status)


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
        try:
            r = get(self.DeviceInfoURL)
        except ConnectionError as e:
            logging.warn("Request to local Plantronics API failed", e)
            pass

        if r.status_code == 200:
            if r.json()["isError"] is True:
                logging.warn(r.json()["Err"]["Description"])
            else:
                self.deviceInfo = r.json()
            return self.deviceInfo
        else:
            logging.error("Response should have status code 200, but was:", r.status)

    def get_callmanager_state(self):
        try:
            r = get(self.CallManagerURL)
        except ConnectionError as e:
            logging.warn("Request to local Plantronics API failed", e)
            pass

        if r.status_code == 200:
            if r.json()["isError"] is True:
                logging.warn(r.json()["Err"]["Description"])
            else:
                self.callManagerInfo = r.json()
            return self.callManagerInfo
        else:
            logging.error("Response should have status code 200, but was:", r.status)
