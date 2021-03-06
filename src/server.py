#!flask/bin/python
#
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
#

import os, sys
import pigpio
from xml.dom import minidom
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder=".", static_folder='.', static_url_path='')

path = os.path.abspath(os.path.dirname(sys.argv[0]))
print "path="+path

@app.route('/<path:path>')
def send_file(path):
    return app.send_static_file(path)

@app.route('/')
def main():
    return render_template('index.html')

#
# GPIO init
#
pi = pigpio.pi()

pins = {
   2 : {'name' : 'blue', 'state' : 0},
   4 : {'name' : 'red',  'state' : 0}
}
for pin in pins:
     pi.write(pin, pins[pin]['state'])

#
# Rest Services
#
@app.route('/pwm', methods=['POST'])
def post_pwm():
    pin=''
    if 'pin' in request.args:
        pin=int(request.args.get('pin'))

        if 'value' in request.args:
            value=float(request.args.get('value'))
            print "LED "+str(pin)+ " " + str(value)
            pi.set_PWM_dutycycle(pin, value * 255)

    return "LED "+str(pin)+ " " + str(value) + "\n"

# /led?pin=1
@app.route('/led', methods=['POST'])
def post_led():
    pin=''
    if 'pin' in request.args:
        pin=int(request.args.get('pin'))

        if 'value' in request.args:
            value=request.args.get('value')
            if value == 'on':
                print "LED "+str(pin)+" on"
                pi.write(pin, 1)
            else:
                print "LED "+str(pin)+" off"
                pi.write(pin, 0)

    return "pin=" + str(pin)

# /gpio?pin=1
@app.route('/gpio', methods=['GET'])
def get_gpio():
    pin=''
    if 'pin' in request.args:
        pin=request.args.get('pin')
    return "pin=" + pin

@app.route('/code/<filename>', methods=['GET'])
def get_code(filename):
    return app.send_static_file("code/" + filename)

@app.route('/code/<filename>', methods=['PUT'])
def put_code(filename):
    xml = minidom.parseString(request.data.decode("utf-8")).toprettyxml(indent="  ")
    file = open(path + "/code/" + filename,'w')
    file.write(xml)
    file.close()
    return ""

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)
