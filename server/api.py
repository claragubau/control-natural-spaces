import os
import base64
import locale
from datetime import datetime

from flask import Flask
from flask import render_template
from flask import request, jsonify, make_response

locale.setlocale(locale.LC_TIME, 'ca_ES.ISO8859-15')
app = Flask(__name__)

plates = list()
os.makedirs('detections', exist_ok=True)

@app.route('/')
def index():
    return render_template("./index.html", plates=plates)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/v1/detection', methods=['POST'])
def create_plate():
    now = datetime.now()
    date = now.strftime("%d %B %Y %H:%M:%S")
    plate = request.values['plate']
    img_data = request.values['image']
    img_path = "detections/{}_{}.png".format(plate, date)
    with open(img_path, "wb") as fh:
        fh.write(base64.decodebytes(img_data))
    
    new_plate = {
        'plate': plate,
        'date': date,
        'image': img_path,
    }

    plates.append(new_plate)
    return jsonify({'plate': plate}), 201


if __name__ == '__main__':
    app.run(host='192.168.0.15', debug=True)
