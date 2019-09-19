import time
import pychromecast

def message_cast(url):
    chromecasts = pychromecast.get_chromecasts()
    print([cc.device.friendly_name for cc in chromecasts])

    cast = next(cc for cc in chromecasts if cc.device.friendly_name == "Kitchen display")
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
