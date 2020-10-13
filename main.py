#!/usr/bin/python

import simpleaudio
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()


def on_connect(client, data, flags, rc):
    client.subscribe("praise/count", 1)


def on_message(client, data, msg):
    print("Praise received!")
    wav_obj = simpleaudio.WaveObject.from_wave_file("osaka-loopline.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

CHANNEL_TOKEN = os.environ.get("BEEBOTTE_CHANNEL_TOKEN")

client.username_pw_set("token:" + CHANNEL_TOKEN)
client.connect("mqtt.beebotte.com", 1883, 60)

print("Connected to beebotte!")

client.loop_forever()
