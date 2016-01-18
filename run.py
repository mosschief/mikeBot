__author__ = 'mossc'
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response
from flask import session as motorSwitch
from flask.ext.basicauth import BasicAuth
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import motor
import os
from thread import start_new_thread

app = Flask(__name__)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

APPLICATION_NAME = "mikeBot"
app.config['BASIC_AUTH_USERNAME'] = 'test'
app.config['BASIC_AUTH_PASSWORD'] = 'test'

basic_auth = BasicAuth(app)

def startCamera():
    os.system("mkdir /tmp/stream")
    os.system("raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0 &")


def startStream():
    os.system('LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www"')

@app.route('/', methods=['GET','POST', 'OPTIONS'])
@basic_auth.required
@crossdomain(origin='*')
def front():

    motorSwitch["right"] = 0
    motorSwitch["left"] = 0


    return render_template("drive.html")

@app.route('/drive/', methods=['POST', 'GET', 'OPTIONS'])
@crossdomain(origin='*')
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
        start_new_thread(startCamera,())
        start_new_thread(startStream,())
        app.run(host='0.0.0.0', port=5000)

    finally:

        print("System shutting down")
        motor.rightStop()
        motor.leftStop()

