from flask import Flask, escape, request
from astor_real_estate import *
import astor_tags
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

@app.route('/mailing_address/<bbl>')
def mailing_address(bbl):
    result = get_mailing_address(bbl)
    return result

@app.route('/add_tax_tag/<propertyid>', methods=['POST'])
def add_tax_tag(propertyid):
    result = 'request_method is ' + request.method
    if request.method == 'POST':
        username = request.json['username']
        tag = request.json['tag']
        result = astor_tags.add_tax_tag(propertyid, username, tag)
    return result

@app.route('/tax_tags/', defaults={'propertyid': None},  methods=['POST', 'GET'])
@app.route('/tax_tags/<propertyid>', methods=['POST'])
def tax_tags(propertyid):
    result = None
    if request.method == 'POST':
        username = request.json['username']
        result = astor_tags.get_tax_tags(propertyid, username)
        pass
    return result

@app.route('/delete_tax_tag/<propertyid>', methods=['POST'])
def delete_tax_tag(propertyid):
    result = 'SUCCESS'
    if request.method == 'POST':
        username = request.json['username']
        tag = request.json['tag']
        result = astor_tags.delete_tax_tag(propertyid, username, tag)
    return result

@app.route('/property_tags/', defaults={'propertyid': None},  methods=['POST', 'GET'])
@app.route('/property_tags/<propertyid>',  methods=['POST', 'GET'])
def property_tags(propertyid):
    result = astor_tags.get_property_tags(propertyid)
    return result

@app.route('/property_tag_list/', methods=['POST', 'GET'])
def unique_property_tags():
    result = astor_tags.property_tag_list()
    return result
