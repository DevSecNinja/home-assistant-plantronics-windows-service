from http.client import HTTPConnection

import json


class PLTDevice:
    def __init__(self, spokes, uid):
        self.AttachURL = "/Spokes/DeviceServices/Attach?uid=" + uid
        self.attached = False
        self.session = None
        self.uid = uid
        self.spokes = spokes

    def attach(self):
        self.spokes.conn.request("GET", self.AttachURL)
        r = self.spokes.conn.getresponse()
        if r.status == 200:
            response = r.read().decode("utf-8")
            print(response)
            response = json.loads(response)
        if response["isError"] is False:
            self.attached = True
            self.session = response["Result"]

    def release(self):
        self.ReleaseURL = "/Spokes/DeviceServices/Release?sess=" + self.session
        self.spokes.conn.request("GET", self.ReleaseURL)
        r = self.spokes.conn.getresponse()
        if r.status == 200:
            response = r.read().decode("utf-8")
            response = json.loads(response)
            if response["isError"] is False:
                self.attached = False
                self.session = None

    def get_events(self, queue=0):
        eventsURL = (
            "/Spokes/DeviceServices/Events?sess="
            + self.session
            + "&queue="
            + str(queue)
        )
        self.spokes.conn.request("GET", eventsURL)
        r = self.spokes.conn.getresponse()
        if r.status == 200:
            response = r.read().decode("utf-8")
            response = json.loads(response)
            print(response)


class Spokes:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "32017"
        self.conn = HTTPConnection(self.host + ":" + self.port)
        self.DeviceInfoURL = "/Spokes/DeviceServices/Info"
        self.CallManagerURL = "/Spokes/CallServices/CallManagerState"
        self.deviceInfo = None
        self.callManagerInfo = None

    def get_device_info(self):
        self.conn.request("GET", self.DeviceInfoURL)
        r = self.conn.getresponse()
        if r.status == 200:
            response = r.read()
            str_response = response.decode("utf-8")
            response = json.loads(str_response)
            if response["isError"] is True:
                print(response["Err"]["Description"])
            else:
                self.deviceInfo = response
        return self.deviceInfo

    def get_callmanager_state(self):
        self.conn.request("GET", self.CallManagerURL)
        r = self.conn.getresponse()
        if r.status == 200:
            response = r.read()
            str_response = response.decode("utf-8")
            response = json.loads(str_response)
            if response["isError"] is True:
                print(response["Err"]["Description"])
            else:
                self.callManagerInfo = response
        return self.callManagerInfo
