from flask import Flask, escape, request
from astor_real_estate import *
from astor_search import *
from covid.covid import *
import astor_tags
import json
app = Flask(__name__)

if __name__ == "__main__":
    app.run()

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

@app.route('/taxcert_neighborhoods/')
def taxcert_neighborhoods():
    result = get_taxcert_neighborhoods()
    return result

@app.route('/get_property_search/<addr>')
def get_property_search(addr):
    result = search_address(addr)
    return result

@app.route('/covid_data/<country>')
def covid_data(country=None):
    result = get_covid_data(country)
    return result

@app.route('/covid_data/')
def all_covid_data():
    result = get_covid_data()
    return result

@app.route('/state_model/<state>')
def state_model(state=None):
    result = get_state_timeline(state)
    return result

@app.route('/state_historic_data/<state>')
def state_historic_data(state=None):
    result = get_historic_data(state)
    return result

@app.route('/state_stats/<state>')
def state_stats(state=None):
    result = get_state_stats(state)
    return result

@app.route('/covid_params/')
def covid_params():
    result = get_covid_parameters()
    return result

