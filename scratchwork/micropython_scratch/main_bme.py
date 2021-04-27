from machine import Pin
from time import sleep
import utime


#this is just used to test resets
led = Pin(2,Pin.OUT)
ii = 0
while ii < 10:
    led.value(not led.value())
    sleep(0.5)
    ii = ii + 1
    

#### Code for BME280
from machine import I2C, Pin
import BME280
i2c = I2C(scl=Pin(22), sda=Pin(21), freq = 10000)
bme = BME280.BME280(i2c = i2c)


### code to update to server
import urequests
import json
import gc

#can generate userandpass string on another computer using:
#from base64 import b64encode
#b64encode(b"$AUTHENTICATED_USERNAME:$AUTHENTICATED_PASSWORD").decode("ascii")
userAndPass = "$ENCODED_OUTPUT"
headers = { 'Authorization' : 'Basic %s' %  userAndPass , 'Content-Type' : 'application/x-www-form-urlencoded','Connection' : 'close'}

#our main loop is defined here. this will run continuously.
while True:

    #double-check that the wifi is connected. if not we'll connect
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('$WIFI_SSID', '$WIFI_PASSWORD')
        #optional: reserve an IP address on your router, and hard-code it here. this can sometimes resolve network connectivity problems.
        #check the docs for ifconfig and your router settings to see what values will work on your setup.
        #sta_if.ifconfig(('$IN_1', '$IN_2', '$IN_3', '$IN_4'))

        while not sta_if.isconnected():
            pass
           
    #read data. convert c to f while we're at it. notice how easy the library makers this.
    temperature=0
    humidity=0
    pressure=0
    for jj in range(20):
        temperature = temperature+float(bme.temperature.strip('C'))*9/5+32
        humidity = humidity + float(bme.humidity.strip('%'))
        pressure = pressure + float(bme.pressure.strip('hPa'))
        sleep(1)
    #average our data
    temperature = temperature / 20
    humidity = humidity / 20
    pressure = pressure / 20
    
    #these values never change
    location = 'desk'
    wetness = 0
    
    #send our data to our server, including our authentication credentials in the http POST
    #in case we get an error, make sure we close the response.
    try:
        resp = urequests.post('https://www.scratchwork.xyz/SQL_API/',data='temperature='+str(temperature)+'&humidity='+str(humidity)+'&wetness='+str(wetness)+'&pressure='+str(pressure)+'&location='+location,headers = headers)
    except Exception as e:
        if isinstance(e, OSError) and resp:
            resp.close()
    
    
    #just in case there are memory problems
    gc.collect()

