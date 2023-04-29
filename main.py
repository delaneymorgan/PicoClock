from machine import Pin
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P8
from pimoroni import RGBLED, Button
import ujson
import network
import time
import urequests
import ntptime

from config import config


class PicoClock(object):
    def __init__(self, display, config):
        """
        construct the clock

        :param display: the pico display object
        :param config: the clock's configuration
        """
        self.display = display
        self.config = config
        self.buttons = dict(tl=Button(12), tr=Button(13), bl=Button(14), br=Button(15))
        self.bg_colour = self.colour_pen(config["bg_colour"])
        self.time_colour = self.colour_pen(config["time_colour"])
        self.button_press = 0
        self.wlan = None
        self.reconnect()
        print(self.config)
        ntptime.host = self.config["ntp_host"]
        ntptime.settime()
        self.last_time_check = 0
        return

    def check_backlight(self, now):
        """
            perform some clever ToD and even MoY calcs to determine backlight level

            @param now the current time as a tuple
        """
        time_24 = now[3] * 100 + now[4]
        if (time.time() - self.button_press) > self.config["hold_duration"]:
            if (time_24 >= self.config["dim_stop"]) and (time_24 < self.config["dim_start"]):
                self.display.set_backlight(self.config["brightness_full"])
            else:
                self.display.set_backlight(self.config["brightness_dim"])
        else:
            self.display.set_backlight(self.config["brightness_full"])
        return

    def reconnect(self):
        """
        reconnect to the LAN

        :return: None
        """
        try:
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)
            self.wlan.connect(self.config["wifi_ssid"], self.config["wifi_password"])
        except Exception as ex:
            print(type(ex))
        return

    def colour_pen(self, colour_string):
        """
        create a colour pen from the specified colour string

        :param colour_string: a hex colour string, i.e. "#000000"
        :return: the new colour pen
        """
        colour_string = colour_string.strip("#")
        red = int(colour_string[:2], 16)
        green = int(colour_string[2:4], 16)
        blue = int(colour_string[4:], 16)
        colour_pen = self.display.create_pen(red, green, blue)
        return colour_pen

    def display_time(self, now, colon_on):
        """
        display the time

        :param now: the current local time as a dictionary
        :param colon_on: True => display colon, False => don't display colon
        :return:
        """
        local_time = now["local"]
        self.display.set_pen(self.bg_colour)
        self.display.clear()
        display_width, display_height = self.display.get_bounds()
        middle_x = int(display_width / 2)
        middle_y = int(display_height / 2)
        self.display.set_font(self.config["time_font"])
        self.display.set_thickness(self.config["time_thickness"])
        self.display.set_pen(self.time_colour)
        hour_str = "%02d" % local_time["hour"]
        min_str = "%02d" % local_time["min"]
        hour_width = self.display.measure_text(hour_str, scale=self.config["time_scale"])
        colon_width = self.display.measure_text(":", scale=self.config["time_scale"])
        x = int(middle_x - colon_width / 2)
        if (not self.config["blink_colon"]) or colon_on:
            self.display.text(":", x, middle_y, scale=self.config["time_scale"])
        x = int(middle_x - hour_width - colon_width / 2)
        if self.config["12_hours"]:
            local_time["hour"] = local_time["hour"] % 12
        hour_str = "%2d" % local_time["hour"]  # we only needed leading zero for calculations
        self.display.text(hour_str, x, middle_y, scale=self.config["time_scale"])
        x = int(middle_x + colon_width)
        self.display.text(min_str, x, middle_y, scale=self.config["time_scale"])
        return

    def check_time(self):
        now = time.time()
        duration = now - self.last_time_check
        if duration > 5:
            self.last_time_check = now
            try:
                response = urequests.get(url=self.config["time_server_url"])
                print(response)
                rich_time = {}
                return rich_time
            except OSError as ex:
                print(ex)
                self.reconnect()
        return None

    def run(self):
        """
        The clock's main loop
        """
        colon_on = True
        while True:
            tick_now = time.time()
            time_now = self.check_time()
            if time_now is not None:
                self.check_backlight(tick_now)
                self.display_time(time_now, colon_on)
                self.display.update()
            for count in range(0, 10):
                for name, button in self.buttons.items():
                    if button.read():
                        self.button_press = tick_now()
                        break
                else:
                    time.sleep(0.1)
                    continue
                break
            colon_on = colon_on ^ True
        return


def quieten_leds():
    pico_led = Pin("LED", Pin.OUT)
    pico_led.off()
    pimoroni_led = RGBLED(6, 7, 8)
    pimoroni_led.set_rgb(0, 0, 0)
    return


def main():
    quieten_leds()
    display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P8)
    pico_clock = PicoClock(display, config)
    pico_clock.run()
    return


main()
