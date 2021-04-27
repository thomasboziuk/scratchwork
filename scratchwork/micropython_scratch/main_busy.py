from machine import Pin
from time import sleep
led = Pin(2,Pin.OUT)
ii = 0
while ii < 10:
    led.value(not led.value())
    sleep(0.5)
    ii = ii + 1
    
import utime


####Code for Dispaly
from machine import I2C, Pin
import ssd1306
i2c = I2C(scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
display.text("Reading... ...",1,1)
display.show()


#### Code for 9-axis device
# from machine import I2C, Pin
# from mpu9250 import MPU9250
# 
# i2c = I2C(scl=Pin(22), sda=Pin(21))
# sensor = MPU9250(i2c)
# 
# print("MPU9250 id: " + hex(sensor.whoami))
# 
# ii = 0
# while ii < 5:
#     print(sensor.acceleration)
#     print(sensor.gyro)
#     print(sensor.magnetic)
# 
#     utime.sleep_ms(1000)
#     ii = ii + 1
# #

### code to update to server
# import urequests
# import json
# import gc
# #can generate userandpass string on another computer using:
# #from base64 import b64encode
# #b64encode(b"API_requester:RequesterPassword").decode("ascii")
# userAndPass = 'QVBJX3JlcXVlc3RlcjpSZXF1ZXN0ZXJQYXNzd29yZA=='
# headers = { 'Authorization' : 'Basic %s' %  userAndPass , 'Content-Type' : 'application/x-www-form-urlencoded','Connection' : 'close'}
# 
# 
# for ii in range(10):
#     #make fake environmental data using accelerometer
#     (temperature,humidity,pressure)=sensor.acceleration
#     location = 'basement'
#     wetness = 0
#     urequests.post('https://www.scratchwork.xyz/SQL_API/',data='temperature='+str(temperature)+'&humidity='+str(humidity)+'&wetness='+str(wetness)+'&pressure='+str(pressure)+'&location='+location,headers = headers)
#     print(ii)
#     sleep(20)
#     gc.collect()
# 
