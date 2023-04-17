from random import randint
import numbers
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

def getSourceData(filename):
    # Read Line by Line of the current file:
    with open(filename, mode='r') as f:
        result = f.read().strip()

    return result

def binToHex(bin):
    return ''.join([hex(int(''.join(map(str, bin[i:i+4])), 2))[2:] for i in range(0, len(bin), 4)])

class RandomNums(Resource):
    # methods go here
    def get(self):
        i = 0
        quantity = 1
        numBits = 1
        quantity = request.args.get('quantity')
        numBits = request.args.get('numBits')
        if not isinstance(quantity, numbers.Number) or not isinstance(numBits, numbers.Number):
            return 'No Letters allowed!', 403 
        result = ''

        for i in range(0, int(quantity)):
            rand = randint(0, 25300000)
            result += str(rand)

        return binToHex(result)
    pass

api.add_resource(RandomNums, '/randomNum/getRandom')

if __name__ == '__main__':
     app.run()