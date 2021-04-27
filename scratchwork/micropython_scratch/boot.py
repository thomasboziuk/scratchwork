# This file is executed on every boot (including wake-boot from deepsleep)

import network
sta_if = network.WLAN(network.STA_IF)



if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('$WIFI_SSID', '$WIFI_PASSWORD')
    #optional: reserve an IP address on your router, and hard-code it here. this can sometimes resolve network connectivity problems.
    #check the docs for ifconfig and your router settings to see what values will work on your setup.
    #sta_if.ifconfig(('$IN_1', '$IN_2', '$IN_3', '$IN_4'))
    while not sta_if.isconnected():
        pass
