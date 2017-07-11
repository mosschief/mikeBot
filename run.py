__author__ = 'mossc'
from flask import Flask, render_template, url_for, request, Response, redirect, flash, jsonify, make_response
from flask import session as motorSwitch
from flask.ext.basicauth import BasicAuth
from datetime import timedelta
from flask import make_response, request, current_app
import motor
import os
from thread import start_new_thread
from flask.ext.cors import CORS
import subprocess
import requests

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
APPLICATION_NAME = "mikeBot"
app.config['BASIC_AUTH_USERNAME'] = 'test'
app.config['BASIC_AUTH_PASSWORD'] = 'test'

basic_auth = BasicAuth(app)

def startVideo():

    subprocess.call('export LD_LIBRARY_PATH=. ; ./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -x 640 -y 480 -fps 15 -vf -hf"', shell=True, cwd='/home/pi/mjpg-streamer/mjpg-streamer-experimental')
# add audio stream subprocess
def startAudio():
    subprocess.call('sudo darkice', shell=True, cwd='/home/pi/mjpg-streamer/mjpg-streamer-experimental')

@app.route('/', methods=['GET','POST'])
@basic_auth.required
def front():

    motorSwitch["right"] = 0
    motorSwitch["left"] = 0
    myIP = requests.get('https://api.ipify.org').text
    audio = 'http://' + myIP + ':8000/live96'
    video = 'http://' + myIP + ':8080/?action=stream'
    return render_template("drive.html", videoStreamAddress=video, audioStreamAddress=audio)

@app.route('/drive/', methods=['POST', 'GET'])
def drive():
    if request.method == 'POST':
        global lookCurrent
        if request.form["right"] and request.form["left"]:
            motorSwitch['right'] = int(request.form["right"])
            motorSwitch['left'] = int(request.form["left"])
        motorSwitch['speed'] = request.form["speed"]
        if motorSwitch['right'] == 1:
            myMotor.rightForward()
        if motorSwitch['left'] == 1:
            myMotor.leftForward()
        if motorSwitch['right'] == 0:
            myMotor.rightStop()
        if motorSwitch['left'] == 0:
            myMotor.leftStop()
        if motorSwitch['right'] == -1:
            myMotor.rightBackward()
        if motorSwitch['left'] == -1:
            myMotor.leftBackward()
        if motorSwitch['speed'] == 'up':
                myMotor.lookUp()
        if motorSwitch['speed'] == 'down':
                myMotor.lookDown()
        return "Ok", 200

    return redirect(url_for('front'))

if __name__ == '__main__':
    global lookCurrent
    lookCurrent = 0
    speedCurrent = 150
    myMotor = motor.Motor()

    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('mikeBot.crt', 'mikeBot.key')
    app.secret_key = 'super secret key'
    # add ssl_context = context to get https on flask server
    app.debug = False
    try:
        start_new_thread(startVideo, ())
        start_new_thread(startAudio, ())
        app.run(host='0.0.0.0', port=5000, threaded=True)

    finally:
        myMotor.shutDown()
        print("System shutting down")



