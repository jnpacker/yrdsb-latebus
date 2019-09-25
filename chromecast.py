import time
import pychromecast

def message_cast(url):
    chromecasts = pychromecast.get_chromecasts()

    for cast in chromecasts:
        print(cast.device.friendly_name)
        # Start worker thread and wait for cast device to be ready
        cast.wait()
        print(cast.device)

        print(cast.status)

        mc = cast.media_controller
        mc.play_media(url, 'audio/m4p3')
        mc.block_until_active()
        print(mc.status)

        mc.pause()
        time.sleep(5)
        mc.play()
