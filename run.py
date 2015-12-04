__author__ = 'mossc'
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response
from flask import session as motorSwitch
from flask.ext.basicauth import BasicAuth
from OpenSSL import SSL
import ssl
'''import motor'''

app = Flask(__name__)

APPLICATION_NAME = "mikeBot"
app.config['BASIC_AUTH_USERNAME'] = 'test'
app.config['BASIC_AUTH_PASSWORD'] = 'test'

basic_auth = BasicAuth(app)

@app.route('/', methods=['GET','POST'])
@basic_auth.required
def front():

    motorSwitch["right"] = 0
    motorSwitch["left"] = 0


    return render_template("drive.html")


@app.route('/drive/', methods=['POST', 'GET'])
def drive():

    if request.method == 'POST':
        motorSwitch['right'] = request.form["right"]
        motorSwitch['left'] = request.form["left"]
        print(motorSwitch['right'])
        print(motorSwitch['left'])

        '''
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
        '''
        return "Ok", 200

    return redirect(url_for('front'))




if __name__ == '__main__':

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('mikeBot.crt', 'mikeBot.key')
    app.secret_key = 'super secret key'
    # add ssl_context = context to get https on flask server
    app.debug = True
    try:
        app.run(host='0.0.0.0', port=5000)

    finally:
        motor.rightStop()
        motor.leftStop()
        print("System shutting down")

