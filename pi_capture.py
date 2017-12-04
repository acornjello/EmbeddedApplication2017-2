import picamera
import time

with picamera.PiCamera() as camera :
    camera.resolution = (1024, 768)
    camera.start_preview()
    
    time.sleep(2)

    camera.capture('foo.jpg', resize=(320,240))
