import irswar
import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

# default periodic delay: 10 seconds
delay = int(os.getenv('DELAY'))
while True:
    output = irswar.send_irs_request()
    if "AVAILABLE" in output:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        output = f"{current_time}\n{output}"
        webhook_url = os.getenv('WEBHOOK_URL')
        print(webhook_url)
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

