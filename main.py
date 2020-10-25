from plantronics import Spokes

s = Spokes()
state = s.get_callmanager_state()

# Output call manager state
print(state["Result"]["HasActiveCall"])

# TODO: Send Call Manager state to Home Assistant

# TODO: Create Windows Service