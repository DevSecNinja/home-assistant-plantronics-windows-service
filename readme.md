# Home Assistant Plantronics Windows Service

Welcome! This Python based Windows Service communicates the status of your Plantronics headset to Home Assistant.

## Requirements
- Plantronics Hub
- Ensure you can browse to the CallManager state URL `http://127.0.0.1:32017/Spokes/CallServices/CallManagerState/` and confirm that the `HasActiveCall` status will change when you are in a call.

## How to
- Open a PowerShell window as administrator and run:

```` powershell
pip install -r .\requirements.txt
````
Make sure that the packages show up under `C:\Program Files (x86)\Python*\Lib\site-packages` as the Windows Service needs to access it.

- Run the ![postinstall.py](https://github.com/mhammond/pywin32/blob/master/pywin32_postinstall.py) from the PowerShell console with administrator privileges.

## Troubleshooting
- In case you receive the error `Error starting service: The service did not respond to the start or control request in a timely fashion` during the start of the service, make sure to have the `pywintypes36.dll` file available from the `C:\Program Files (x86)\Python*\Lib\site-packages\win32` folder. In case the file is missing, copy it from the `C:\Program Files (x86)\Python*\Lib\site-packages\pywin32_system32` folder.
