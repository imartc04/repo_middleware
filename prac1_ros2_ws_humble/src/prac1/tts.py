
import time
from gtts import gTTS
from pygame import mixer

slow = False
text = "Hello World"
language = "en"
gtts_file = "/tmp/gtts_tmp_file.mp3"

gtts_obj = gTTS(text=text,
                lang=language, slow=slow)

gtts_obj.save(gtts_file)


mixer.init()
mixer.music.load(gtts_file)
mixer.music.play()

while mixer.music.get_busy():
    time.sleep(1)
