__author__ = 'mossc'
from flask import Flask, render_template, url_for, request, Response, redirect, flash, jsonify, make_response
from flask import session as motorSwitch
from flask.ext.basicauth import BasicAuth
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import motor
import os
from thread import start_new_thread
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
APPLICATION_NAME = "mikeBot"
app.config['BASIC_AUTH_USERNAME'] = 'test'
app.config['BASIC_AUTH_PASSWORD'] = 'test'

basic_auth = BasicAuth(app)

def startStream():

    os.chdir('/var/www/mjpg-streamer/mjpg-streamer-experimental')
    # os.system('export LD_LIBRARY_PATH=.')
    # os.system('./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -fps 15 -vf -hf"')
    # p=os.system('ls')
    # print p


@app.route('/', methods=['GET','POST'])
@basic_auth.required
def front():

    motorSwitch["right"] = 0
    motorSwitch["left"] = 0


    return render_template("drive.html")

@app.route('/drive/', methods=['POST', 'GET'])
def drive():

    if request.method == 'POST':
        global speedCurrent
        if request.form["right"] and request.form["left"]:
            motorSwitch['right'] = int(request.form["right"])
            motorSwitch['left'] = int(request.form["left"])
        motorSwitch['speed'] = request.form["speed"]
        print("motor switch right: " + str(motorSwitch['right']))
        print("motor switch left: " + str(motorSwitch['left']))


        if motorSwitch['right'] == 1:
            motor.rightForward()
        if motorSwitch['left'] == 1:
            motor.leftForward()
        if motorSwitch['right'] == 0:
            motor.rightStop()
        if motorSwitch['left'] == 0:
            motor.leftStop()
        if motorSwitch['right'] == -1:
            motor.rightBackward()
        if motorSwitch['left'] == -1:
            motor.leftBackward()
        if motorSwitch['speed'] == 'up':

            tmpMessage = motor.speedUp(speedCurrent)
            if type(tmpMessage) == 'int':
                speedCurrent = tmpMessage
            else:
                print tmpMessage
        if motorSwitch['speed'] == 'down':
            tmpMessage = speedCurrent = motor.speedDown(speedCurrent)
            if type(tmpMessage) == 'int':
              speedCurrent = tmpMessage
            else:
              print tmpMessage

        return "Ok", 200

    return redirect(url_for('front'))

if __name__ == '__main__':
    global speedCurrent
    speedCurrent = 150

    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('mikeBot.crt', 'mikeBot.key')
    app.secret_key = 'super secret key'
    # add ssl_context = context to get https on flask server
    app.debug = False
    try:

        start_new_thread(startStream, ())
        app.run(host='0.0.0.0', port=5000, threaded=True)

    finally:

        print("System shutting down")
        motor.rightStop()
        motor.leftStop()


