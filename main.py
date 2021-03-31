#!/usr/bin/python

import asyncio
from time import sleep
import simpleaudio
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
import concurrent.futures

load_dotenv()

played = False
DEBOUNCE_DELAY = os.environ.get("DEBOUNCE_DELAY")


def debounce(delay):
    global played
    while True:
        played = False
        sleep(delay)


async def debounce_async(loop, executor):
    global played
    loop.run_in_executor(executor, debounce, DEBOUNCE_DELAY)


def on_connect(client, data, flags, rc):
    client.subscribe("praise/count", 1)
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    loop.run_until_complete(debounce_async(loop, executor))


def on_message(client, data, msg):
    global played
    if played == False:
        wav_obj = simpleaudio.WaveObject.from_wave_file("osaka-loopline.wav")
        wav_obj.play()
        played = True


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

CHANNEL_TOKEN = os.environ.get("BEEBOTTE_CHANNEL_TOKEN")

client.username_pw_set("token:" + CHANNEL_TOKEN)
client.connect("mqtt.beebotte.com", 1883, 60)

print("Connected to beebotte!")

client.loop_forever()
