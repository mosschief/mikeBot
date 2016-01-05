__author__ = 'mossc'
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response
from flask import session as motorSwitch
from flask.ext.basicauth import BasicAuth

import motor
import subprocess

app = Flask(__name__)

APPLICATION_NAME = "mikeBot"
app.config['BASIC_AUTH_USERNAME'] = 'test'
app.config['BASIC_AUTH_PASSWORD'] = 'test'

basic_auth = BasicAuth(app)

@app.route('/', methods=['GET','POST','OPTIONS'])
@crossdomain(origin='*')
@basic_auth.required
def front():

    motorSwitch["right"] = 0
    motorSwitch["left"] = 0
    # subprocess.call(['mkdir', '/tmp/stream'])
    # subprocess.call(['rapistill', '--nopreview', '-w', '640', '480', '-q', '5', '-o', '/tmp/stream/pic.jpg', '-tl', '100', '-t', '9999999', '-th', '0:0:0', '&'])
    # subprocess.call(['LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer', '-i', '"input_file.so -f /tmp/stream -n pic.jpg"', '-0', '"output_http.so -w /usr/local/www"'])
    return render_template("drive.html")

@app.route('/drive/', methods=['POST', 'GET'])
def drive():

    if request.method == 'POST':

        motorSwitch['right'] = int(request.form["right"])
        motorSwitch['left'] = int(request.form["left"])
        motorSwitch['speed'] = int(request.form["speed"])
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
            motor.speedUp()
        if motorSwitch['speed'] == 'down':
            motor.speedDown()

        return "Ok", 200

    return redirect(url_for('front'))

s
if __name__ == '__main__':

    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('mikeBot.crt', 'mikeBot.key')
    app.secret_key = 'super secret key'
    # add ssl_context = context to get https on flask server
    app.debug = True
    try:
        app.run(host='0.0.0.0', port=5000)

    finally:

        print("System shutting down")
        motor.rightStop()
        motor.leftStop()

