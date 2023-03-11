# PicoClock
A NTP-connected clock for the RPi Pico

Some traps:

* Pico W's LED is managed differently to the old Pico
* You will probably need permission to use your machine's serial port
  * usermod -a -G dialout \<username> && sudo reboot
* Pico W supports 2.4GHz only


