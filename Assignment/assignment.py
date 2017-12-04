
from flask import Flask, request
from flask import render_template
from google.cloud import vision
from google.cloud.vision import types

import RPi.GPIO as GPIO
import time
import picamera
import datetime
import io

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)


app = Flask(__name__)

def getGpioState():
    
    state = False
    if GPIO.input(4) == 1:
        state = True
        time.sleep(0.5)
    else:
        state = False
        time.sleep(0.5)
    
    return state

def detect_label(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    return labels

def getDatetime():
    date = datetime.datetime.now()
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    hour = str(date.hour)
    min = str(date.minute)
    sec = str(date.second)

    if int(month) < 10:
        month = '0' + month
    if int(day) < 10:
        day = '0' + day
    if int(hour) < 10:
        hour = '0' + hour
    if int(min) < 10:
        min = '0' + min

    t =  year + month + day + hour + min + sec

    return t

@app.route("/detecting")
def main():
        gpioState = {
               ## 'leds' : getGpioState()
            'result' : getGpioState()
        }
        return render_template('main.html', **gpioState)

@app.route("/camera")
def action():
    filename = getDatetime() + '.jpg'
    
    with picamera.PiCamera() as camera:
	camera.resolution = (1024, 768)
        time.sleep(2)
	camera.capture('./static/'+filename, resize=(320,240))
    
    time.sleep(0.5)
    
    labels = detect_label('./static/'+filename)

    capture = {
            'filename' : filename,
            'labels' : labels
    }
    
    return render_template('camera.html', **capture)



if __name__ == "__main__":
        app.run(host='192.168.0.18', port=8888, debug = True)

