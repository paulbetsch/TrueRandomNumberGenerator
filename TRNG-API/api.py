from random import randint
import numbers
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class RandomNums(Resource):        
    # methods go here
    def get(self):
        i = 0
        quantity = 1
        numBits = 1
        quantity = request.args.get('quantity')
        numBits = request.args.get('numBits')
        if not isinstance(quantity, numbers.Number) and not isinstance(numBits, numbers.Number):
            return 'No Letters allowed!', 403 
        result = [int(quantity)]

        for i in range(0, int(quantity)):
            rand = hex(randint(0, 25300000))
            result.append(rand)

        return result
    pass

api.add_resource(RandomNums, '/randomNum/getRandom')

if __name__ == '__main__':
     app.run()