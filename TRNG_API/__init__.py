import threading
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_cors import CORS
from ..TRNG_Pendel import pendelManager

# Determines if Generating Random Numbers is possible
TRNG_RUNNING = False

# App configs (TODO: change to WSGI before Production)
app = Flask(__name__)
CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
api.prefix = '/trng'

# This Endpoint returns a True Random Number generated by our chaotic pendulum.
# There are two Parameters which changes the returned value:
# 1. quantity: Number of random numbers to get (of equal bit sequence length)
# 2. numBits: Number of random bits in each bit sequence
class GetRandomNums(Resource):
    def get(self):
        global TRNG_RUNNING
        response = ''
        manager = pendelManager.GetInstance()
        # len of result array given by parameter
        quantity = request.args.get('quantity', default=1, type=int)
        #len of the random Bits
        numBits = request.args.get('numBits', default=1, type=int)

        if(not TRNG_RUNNING):
            response = make_response(jsonify({'description': 'system not ready; try init'}), 432)
        else:
            # Call generation from pendelManager
            try:
                result = manager.generateRandomBits(quantity, numBits)
                response = make_response(result, 200)
            except Exception:
                response = make_response(jsonify({'description': 'data generation failed; check noise source'}), 500)
            
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

# This endpoint initializes the TRNG and ensures that the endpoint GetRandomNums works.
class InitRandomNums(Resource):
    def get(self):
        global TRNG_RUNNING
        response = ''
        if(TRNG_RUNNING):
            response = make_response(jsonify({'description': 'system already running'}), 403)
        else:
            manager = pendelManager.GetInstance()
            t = threading.Thread(target=manager.checkFunctionality)
            t.join(timeout=60)
            
            if(pendelManager.BsiInitTestsPassed):
                TRNG_RUNNING = True
                response = make_response(jsonify({'description': 'system initialized'}), 200)
            else:
                TRNG_RUNNING = False
                response = make_response(jsonify({'description': 'functionality not given; check hardware'}), 403)

        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

# This endpoint shuts down the TRNG
class ShutdownRandomNums(Resource):
    def get(self):
        global TRNG_RUNNING
        response = ''
        if(TRNG_RUNNING):
            TRNG_RUNNING = False
            response = make_response(jsonify({'description': 'system shutdown'}), 200)
        else:
            response = make_response(jsonify({'description': 'system already shutdown'}), 403)

        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


api.add_resource(GetRandomNums, '/randomNum/getRandom')
api.add_resource(InitRandomNums, '/randomNum/init')
api.add_resource(ShutdownRandomNums, '/randomNum/shutdown')

if __name__ == '__main__':

     app.run(port=5520)