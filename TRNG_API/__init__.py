import random
import json
import time
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_cors import CORS

# Determines if Generating Random Numbers is possible
TRNG_RUNNING = False

# App configs (TODO: change to WSGI before Production)
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
api.prefix = '/trng'

# This Endpoint returns a True Random Number generated by our chaotic pendulum.
# There are two Parameters which changes the returned value:
# 1. quantity: Number of random numbers to get (of equal bit sequence length)
# 2. numBits: Number of random bits in each bit sequence
class GetRandomNums(Resource):
    def get(self):
        global TRNG_RUNNING
        if(not TRNG_RUNNING):
            return make_response(jsonify({'description': 'system not ready; try init'}), 432)
        # counter for len of result array
        i = 0
        # len of result array given by parameter
        quantity = request.args.get('quantity', default=1, type=int)
        #len of the random Bits
        numBits = request.args.get('numBits', default=1, type=int)
        # calculate the len of the result numbers to fill in leading zeroes if wanted.
        numHexDigits = (numBits + 3) // 4
        #resultArray which will be returned
        result = []

        # Get as many Random Numbers as required
        for i in range(0, quantity):
            # Get Random Bits from NoiseSource
            randomBits = random.getrandbits(numBits)
            # Convert them into hex number
            randomHex = hex(int(randomBits))
            # If necesarry remove leading "0x"
            hexStr = str(randomHex)[2:]
            # Prepend the necessary number of leading zeroes to the hex string
            hexStr = hexStr.zfill(numHexDigits)
            # Append the Hex Number to the array
            result.append(hexStr)
        if(len(result) > 0):
            response = make_response(result, 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            response = make_response(jsonify({'description': 'system deliverd an empty array; check noise source'}), 500)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

# This endpoint initializes the TRNG and ensures that the endpoint GetRandomNums works.
class InitRandomNums(Resource):
    def get(self):
        global TRNG_RUNNING
        if(TRNG_RUNNING):
            response = make_response(jsonify({'description': 'system already running'}), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            # time.sleep(60)
            TRNG_RUNNING = True
            response = make_response(jsonify({'description': 'system initialized'}), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

# This endpoint shuts down the TRNG
class ShutdownRandomNums(Resource):
    def get(self):
        global TRNG_RUNNING
        if(TRNG_RUNNING):
            TRNG_RUNNING = False
            response = make_response(jsonify({'description': 'system shutdown'}), 200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            response = make_response(jsonify({'description': 'system already shutdown'}), 403)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response


api.add_resource(GetRandomNums, '/randomNum/getRandom')
api.add_resource(InitRandomNums, '/randomNum/init')
api.add_resource(ShutdownRandomNums, '/randomNum/shutdown')

if __name__ == '__main__':

     app.run()