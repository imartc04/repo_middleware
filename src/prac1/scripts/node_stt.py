#!/usr/bin/python3
import rclpy
from std_msgs.msg import String

import time
# from gtts import gTTS
# from pygame import mixer

import speech_recognition as sr

def listener_node():
    rclpy.init()
    node = rclpy.create_node('speech_to_text')
    rec = sr.Recognizer()
    seconds = 4

    while True:
        with sr.Microphone() as source:

            print("Calibrating")
            rec.adjust_for_ambient_noise(source, duration=seconds)
            print("Set minimum energy threshold to " + str(rec.energy_threshold))

            print("Listening")
            audio = rec.listen(source, timeout=None, phrase_time_limit=None)
            print("End listening...")
            try:
                text = rec.recognize_google(audio)
                print(format(text))
            except:
                print("Error recognizing")

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    listener_node()
