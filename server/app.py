#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from models import db, Plant
from flask_restful import abort


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])
    
    def post(self):
        data = request.get_json()
        new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201

class PlantByID(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)
        if plant is None:
            abort(404, message="Plant not found")
        return jsonify(plant.to_dict())


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
