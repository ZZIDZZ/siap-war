import irswar
import os
import requests
import json
import time

# default periodic delay: 10 seconds
delay = int(os.environ.get('DELAY'))
while True:
    output = irswar.send_irs_request()
    if "AVAILABLE" in output:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        output = f"{current_time}\n{output}"
        webhook_url = os.environ.get('WEBHOOK_URL')
        url = webhook_url
        data = {
            "content": output
        }
        headers = {
            "Content-Type": "application/json"
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
    else:
        print("Not available")
    time.sleep(delay)

