#!flask/bin/python
#
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
#

from flask import Flask, render_template, request, jsonify
app = Flask(__name__, template_folder=".", static_folder='.', static_url_path='')

@app.route('/<path:path>')
def send_file(path):
    return app.send_static_file(path)

@app.route('/')
def main():
    return render_template('index.html')

#
# Rest Services
#

data = [
    {
        'id': 1
    },
    {
        'id': 2
    }
]

# /gpio?pin=1
@app.route('/gpio', methods=['GET'])
def get_gpio():
    pin=''
    if 'pin' in request.args:
        pin=request.args.get('pin')
    return "pin=" + pin

@app.route('/code', methods=['GET'])
def get_code():
    file = 'current'
    if 'file' in request.args:
        file = request.args.get('file')
    return app.send_static_file(file + '.xml')

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)

