import requests
import time
while True:
    r = requests.get("http://13.60.12.250/actualizar")
    print(r)
    print(r.text)
    time.sleep(60)