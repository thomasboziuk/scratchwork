from machine import Pin
from time import sleep
led = Pin(2,Pin.OUT)
ii = 0
while ii < 20:
    led.value(not led.value())
    sleep(0.5)
    ii = ii + 1
    
import utime
from machine import I2C, Pin
from mpu9250 import MPU9250

i2c = I2C(scl=Pin(22), sda=Pin(21))
sensor = MPU9250(i2c)

ii = 0
while ii < 20:
    print(sensor.acceleration)
    print(sensor.gyro)
    print(sensor.magnetic)

    utime.sleep_ms(1000)
    ii = ii + 1