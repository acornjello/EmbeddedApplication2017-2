from flask import Flask, request, jsonify, render_template
from google.cloud import vision
from google.cloud.vision import types

import RPi.GPIO as GPIO
import time
import picamera
import datetime
import io
import socket
import json

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)


app = Flask(__name__)


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


def detect_label(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    return labels

def detect_faces(path):
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_face_detection]
    # [START migration_image_file]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    # [END migration_image_file]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
    return faces


@app.route("/challenge")
def challenge():

    return render_template('challenge.html');


@app.route("/video1")
def challenge_video():

    return render_template('video1.html')


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/echo2/', methods=['GET'])
def echo():
    cnt = request.args.get('cnt', 0, type=int)
    cnt = 1
    filename = getDatetime() + '.jpg'

    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        time.sleep(2)
        camera.capture('./static/' + filename, resize=(320, 240))

    time.sleep(0.5)
    faces = detect_faces('./static/' + 'surprise.jpg')

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    anger = []
    joy = []
    surprise = []
    sorrow = []


    # for face in faces:
    #     anger.append(likelihood_name[face.anger_likelihood]);
    #     joy.append(likelihood_name[face.joy_likelihood]);
    #     surprise.append(likelihood_name[face.surprise_likelihood]);
    #     sorrow.append(likelihood_name[face.sorrow_likelihood]);
    for face in faces:
        anger.append(face.anger_likelihood);
        joy.append(face.joy_likelihood);
        surprise.append(face.surprise_likelihood);
        sorrow.append(face.sorrow_likelihood);

    ret_data = {"anger": anger,
                "joy" : joy,
                "surprise" : surprise,
                "sorrow": sorrow,
                "detect" : cnt
                }

    return jsonify(ret_data)

@app.route('/echo/', methods=['GET'])
def echo2():
    filename = getDatetime() + '.jpg'

    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        time.sleep(2)
        camera.capture('./static/' + filename, resize=(320, 240))

    time.sleep(0.5)

    labels = detect_label('./static/' + filename)

    capture = []
    for label in labels :
        capture.append(label.description)


    jsonString = json.dumps(capture)
    print(jsonString)

    ret_data = {"value": capture}

    return jsonify(ret_data)



if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect(('google.com', 0))
    ipAddress = s.getsockname()[0]


    app.run(host=ipAddress, port=8888, debug = True)
    s.close()

