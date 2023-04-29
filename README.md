# PicoClock
A Simple Time of Day, "internet-connected" clock for the RPi Pico.

## Introduction:
PicoClock is a simple ToD clock using the [Pimoroni Pico Display Pack 2.0](https://shop.pimoroni.com/products/pico-display-pack-2-0).

PicoClock relies on [LocalTimeServer](https://github.com/delaneymorgan/LocalTimeServer) to get the time as, of course, it has no RTC of its own.
So it must be able to see LocalTimeServer on your local WiFi network.

**NOTE**: Pico W supports _2.4GHz_ WiFi only

## Installation:
Firstly, you will probably need permission to use your machine's serial port.

```shell
  usermod -a -G dialout \<username> && sudo reboot
```

Secondly, you will need the relevant Pimoroni [MicroPython](https://github.com/pimoroni/pimoroni-pico/releases).
Use [this](https://github.com/pimoroni/pimoroni-pico/releases/download/v1.19.18/pimoroni-picow-v1.19.18-micropython.uf2) for the RPi Pico W, 

Perform the usual boot-loader thing to install the interpreter.

You will then need to copy the following files from this repo to the Pico:
* main.py
* config.py

## Configuration:
PicoClock's behaviour is driven by the config.py file.

```python
config = {
  "12_hours": True,
  "bg_colour": "#000000",
  "blink_colon": True,
  "brightness_dim": 0.25,
  "brightness_full": 1.0,
  "dim_start": 1800,
  "dim_stop": 600,
  "hold_duration": 5,
  "time_colour": "#00ff00",
  "time_font": "sans",
  "time_scale": 2.5,
  "time_server_url": "http://LOCALTIMESERVER-ADDRESS:PORT",
  "time_thickness": 5,
  "wifi_password": "MYPASSWORD",
  "wifi_ssid": "MYSSID"
}
```

Where:
* 12_hours - true => 12 hour format, false => 24 hour format
* bg_colour - the background colour in hex colour code (RGB) format
* blink_colon - true => blink, false => don't blink
* brightness_dim - dim brightness setting between (0.0 - 1.0)
* brightness_full - full brightness setting between (0.0 - 1.0)
* dim_start - ToD when dimming starts in 24 hour format (i.e. 1800 = 6pm)
* dim_stop - ToD when dimming stops in 24 hour format (i.e. 600 = 6am)
* hold_duration - duration in seconds to hold full brightness on a button press
* time_colour - the time colour in hex colour code (RGB) format
* time_font - the font to use for time
* time_scale - the scaling to use for the time text
* time_server_url - the address of the local time server
* time_thickness - the thickness of the characters for time text
* wifi_password - the LAN password
* wifi_ssid - the LAN SSID

