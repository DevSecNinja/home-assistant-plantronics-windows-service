# Home Assistant Plantronics Windows Service

Welcome! This Python based Windows Service communicates the status of your Plantronics headset to Home Assistant.

## Requirements
- Plantronics Hub
- Ensure you can browse to the CallManager state URL (http://127.0.0.1:32017/Spokes/CallServices/CallManagerState/) and confirm that the `HasActiveCall` status will change when you are in a call.
