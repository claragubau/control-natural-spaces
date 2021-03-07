import locale
from flask import Flask
from flask import request, jsonify, abort, make_response
from flask import render_template
from datetime import datetime

locale.setlocale(locale.LC_TIME, 'ca_ES.ISO8859-15')
app = Flask(__name__)

plates = list()

@app.route('/')
def index():
    return render_template("./index.html", plates = plates)
@app.route('/', methods=['GET'])


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

@app.route('/v1/detection', methods=['POST'])
def create_plate():
    now = datetime.now()
    date = now.strftime("%d %B %Y %H:%M:%S")
    plate = request.json['plate']
    img_data = request.json['image']
    
    new_plate = {
        'plate': request.json['plate'],
        'date': date,
        'image': 'data:image/jpeg;base64, {}'.format(img_data)
    }

    plates.append(new_plate)
    return jsonify({'plate':plate}), 201


if __name__ == '__main__':
    app.run(host= '192.168.0.15', debug=True)
