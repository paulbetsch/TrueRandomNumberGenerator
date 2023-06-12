from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)


TRNG_RUNNING = False

@app.route('/randomNum/getRandom', methods=['GET'])
def getRandom():
    global TRNG_RUNNING

    quantity = int(request.args.get('quantity', 1))
    numBits = int(request.args.get('numBits', 1))
    result = []

    if not TRNG_RUNNING:
        response = make_response(jsonify({'description': 'system not ready; try init'}), 432)
    else:
        # Generate random numbers here
        for i in range (quantity):
            result.append("123456789ABCDEF")
        time.sleep(5)
        response = make_response(jsonify({'randomNumbers': result, 'status': 'Success'}), 200)

    return response


@app.route('/randomNum/init', methods=['GET'])
def initRandomNums():
    global TRNG_RUNNING
    if TRNG_RUNNING:
        response = make_response(jsonify({'description': 'system already running'}), 409)
    else:
        # Initialize the TRNG here
        # ...
        TRNG_RUNNING = True
        response = make_response(jsonify({'description': 'system initialized'}), 200)

    return response


@app.route('/randomNum/shutdown', methods=['GET'])
def shutdownRandomNums():
    global TRNG_RUNNING

    if TRNG_RUNNING:
        # Shut down the TRNG here
        # ...
        TRNG_RUNNING = False
        response = make_response(jsonify({'description': 'system shutdown'}), 200)
    else:
        response = make_response(jsonify({'description': 'system already shutdown'}), 409)

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5520)
