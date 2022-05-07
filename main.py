#!/usr/bin/python

# import simpleaudio
import os
from time import sleep

import paho.mqtt.client as mqtt
import requests
from dotenv import load_dotenv
from rgbxy import Converter

load_dotenv()

HUE_API = os.environ.get("HUE_API")


converter = Converter()


def on_connect(client, data, flags, rc):
    client.subscribe("praise/count", 1)


def on_message(client, data, msg):
    print("Praise received!")
    # wav_obj = simpleaudio.WaveObject.from_wave_file("osaka-loopline.wav")
    # play_obj = wav_obj.play()
    blink_hue()
    blink_hue()
    blink_hue()
    # play_obj.wait_done()


def blink_hue():
    red_xy = converter.hex_to_xy("ff0000")
    green_xy = converter.hex_to_xy("00ff00")
    blue_xy = converter.hex_to_xy("0000ff")
    white_xy = converter.hex_to_xy("ffffff")

    requests.put(HUE_API + '/groups/1/action',
                 json={"on": True, "bri": 512, "xy": red_xy})
    sleep(0.5)
    requests.put(HUE_API + '/groups/1/action',
                 json={"on": True, "bri": 512, "xy": green_xy})
    sleep(0.5)
    requests.put(HUE_API + '/groups/1/action',
                 json={"on": True, "bri": 512, "xy": blue_xy})
    sleep(0.5)
    requests.put(HUE_API + '/groups/1/action',
                 json={"on": True, "bri": 512, "xy": white_xy})


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

CHANNEL_TOKEN = os.environ.get("BEEBOTTE_CHANNEL_TOKEN")

client.username_pw_set("token:" + CHANNEL_TOKEN)
client.connect("mqtt.beebotte.com", 1883, 60)

print("Connected to beebotte!")

client.loop_forever()
