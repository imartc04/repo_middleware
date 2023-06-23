#!/usr/bin/python3
import rclpy
from std_msgs.msg import String

import time
from gtts import gTTS
from pygame import mixer


def callback(msg):
    print("Received message: {}".format(msg.data))

    tts_file = "/tmp/tts_obj_tmp_file.mp3"
    tts_obj = gTTS(text=msg.data, lang ="en", slow=False)
    
    tts_obj.save(tts_file)
    mixer.init()
    mixer.music.load(tts_file)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(1)

def listener_node():
    rclpy.init()
    node = rclpy.create_node('text_to_speech')
    
    subscriber = node.create_subscription(
        String,
        'text',
        callback,
        10  # Queue size
    )
    subscriber  # Prevent unused variable warning
    
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    listener_node()
