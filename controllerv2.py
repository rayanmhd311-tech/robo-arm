import network
import espnow
import machine
import time
from machine import Pin, PWM
from machine import ADC
from time import sleep, sleep_us

net = network.WLAN(network.STA_IF)
net.active(True)

esp = espnow.ESPNow()
esp.active(True)

peer = b'\x20\x6e\xf1\x08\x4a\xc8' #MA address for receiving esp board
esp.add_peer(peer)

base = ADC(Pin(32))
shoulder = ADC(Pin(33))
head = ADC(Pin(25))

base.atten(ADC.ATTN_11DB)
shoulder.atten(ADC.ATTN_11DB)
head.atten(ADC.ATTN_11DB)

last_angleb = -1
last_angles = -1
last_angleh = -1

maxe = 3300

while True:
    valueb = base.read()
    values = shoulder.read()
    valueh = head.read()
    
    angleb = int((valueb * 2) - 190)
    angles = int((values * 2) - 190)
    angleh = int((valueh * 2) - 190)
    
    angleb = max(0, min(8000, angleb))
    angles = max(0, min(8000, angles))
    angleh = max(0, min(8000, angleh))
    
    data = "{},{},{}".format(angleb, angles, angleh)

    if (abs(angleb - last_angleb) > 90 or
        abs(angles - last_angles) > 90 or
        abs(angleh - last_angleh) > 90):

        esp.send(peer, data.encode())

        last_angleb = angleb
        last_angles = angles
        last_angleh = angleh
    time.sleep(0.03)
    print(angleb)
    print(angles)
    print(angleh)
    print(data)