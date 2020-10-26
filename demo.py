"""Demo file to display what can be done with the Plantronics Hub API."""
from plantronics import Spokes, PLTDevice
import time

spo = Spokes()
dev = PLTDevice(spo, "0123456789")

print("Output of get_callmanager_state")
print(spo.get_callmanager_state())

print("Output of get_device_info")
print(spo.get_device_info())

dev.attach()

try:
    while True:
        dev.get_events()
        time.sleep(1)

finally:
    dev.release()
