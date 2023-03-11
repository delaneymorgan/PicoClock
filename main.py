#!/usr/bin/env python3


from machine import Pin
import mysecrets
import network
import time
import urequests


# ================================================================================


def set_up():
    led = Pin("LED", Pin.OUT)
    led.off()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(mysecrets.SSID, mysecrets.PASSWORD)
    led.on()
    return led

def main_loop(led):
    while True:
        r = urequests.get("http://203.44.160.250:10123")
        print(r.json())
        led.toggle()
        time.sleep(1)
    return


led = set_up()
main_loop(led)
