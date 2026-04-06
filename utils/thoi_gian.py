import time
from datetime import datetime

def lay_timestamp_ms():
    return int(time.time() * 1000)

def ngu_an_toan(giay):
    time.sleep(giay)