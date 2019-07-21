from flask import Flask, escape, request
from astor_real_estate import *
import json

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/nearby_buildings/<bbl>')
def nearby_buildings(bbl):
    result = json.dumps(get_nearby_buildings(bbl))
    return result

@app.route('/similar_buildings/<bbl>')
def similar_buildings(bbl):
    result = json.dumps(get_similar_buildings(bbl))
    return result

@app.route('/building_info/<bbl>')
def building_info(bbl):
    result = get_building_attributes_by_bbl(bbl)
    return result

