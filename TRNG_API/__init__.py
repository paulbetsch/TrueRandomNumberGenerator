from random import randint
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
api.prefix = '/trng'

def getSourceData(filename):
    # Read Line by Line of the current file:
    with open(filename, mode='r') as f:
        result = f.read().strip()

    return result

def binToHex(bin):
    return ''.join([hex(int(''.join(map(str, bin[i:i+4])), 2))[2:] for i in range(0, len(bin), 4)])


class GetRandomNums(Resource):
    # methods go here
    def get(self):
        i = 0
        quantity = request.args.get('quantity', default=1, type=int)
        numBits = request.args.get('numBits', default=1, type=int)
        result = []

        for i in range(0, int(quantity)):
            rand = randint(0, 25300000)
            result.append(hex(rand))

        return result
    pass

class InitRandomNums(Resource):
    # methods go here
    def get(self):
        i = 0
        quantity = request.args.get('quantity', default=1, type=int)
        numBits = request.args.get('numBits', default=1, type=int)
        result = []

        for i in range(0, int(quantity)):
            rand = randint(0, 25300000)
            result.append(hex(rand))

        return result
    pass

class ShutdownRandomNums(Resource):
    # methods go here
    def get(self):
        return jsonify({403, ''})
    pass


api.add_resource(GetRandomNums, '/randomNum/getRandom')
api.add_resource(InitRandomNums, '/randomNum/init')
api.add_resource(ShutdownRandomNums, '/randomNum/shutdown')

if __name__ == '__main__':
     app.run()