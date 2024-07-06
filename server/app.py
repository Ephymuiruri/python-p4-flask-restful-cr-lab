#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        response_body =[plant.to_dict() for plant in plants]
        return make_response(response_body,200)
    def post(self):
        data = request.get_json()
        name = data.get('name')
        image = data.get('image')
        price = data.get('price')

        if not name or not image or not price:
            return make_response("All fields are required", 400)

        plant = Plant(name=name, image=image, price=price)
        db.session.add(plant)
        db.session.commit()

        return make_response(plant.to_dict(), 201)
api.add_resource(Plants,'/plants')  

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get_or_404(plant_id)
        return make_response(plant.to_dict(), 200)
        
api.add_resource(PlantByID,'/plants/<int:plant_id>') 
if __name__ == '__main__':
    app.run(port=5555, debug=True)
