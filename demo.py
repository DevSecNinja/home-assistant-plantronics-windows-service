"""Demo file to display what can be done with the Plantronics Hub API."""
import logging
import sys
import time

from plantronics import PLTDevice, Spokes

# Ensure info log is forwarded to stdout and visible on console
# Changge logging.info to logging.debug in case you want the debug log to output to console
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

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
        spo.get_callmanager_state()
        time.sleep(1)

finally:
    dev.release()
