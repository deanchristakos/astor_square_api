from flask import Flask, escape, request
from astor_real_estate import *
import json
#from app import app

#if __name__ == "__main__":
#    app.run()

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

@app.route('/tax_analysis/<bbl>')
def tax_analysis(bbl):
    result = get_building_tax_analysis(bbl)
    return result

@app.route('/city_comparables/<bbl>')
def city_comparable(bbl):
    result = get_city_tax_comparable_buildings(bbl)
    return result

@app.route('/recommended_comparables/<bbl>')
def recommended_comparable(bbl):
    result = get_recommended_tax_comparable_buildings(bbl)
    return result

@app.route('/combined_comparables/<bbl>')
def combined_comparable(bbl):
    result = get_combined_tax_comparable_buildings(bbl)
    return result