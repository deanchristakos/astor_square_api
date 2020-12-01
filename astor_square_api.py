from flask import Flask, escape, request
import logging
from astor_real_estate import *
from astor_search import *
from covid import *
import astor_tags
import astor_users
import astor_purchases
import json
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

#app = Flask(__name__)
app.logger.setLevel(logging.INFO)

logging.basicConfig(filename='/tmp/flask.log', level=logging.INFO)
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

@app.route('/property_address/<bbl>')
def property_address(bbl):
    result = get_property_address(bbl)
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


@app.route('/add_required_tax_tag/<propertyid>', methods=['POST'])
def add_required_tax_tag(propertyid):
    result = 'request_method is ' + request.method
    if request.method == 'POST':
        username = request.json['username']
        tag = request.json['tag']
        result = astor_tags.add_required_tax_tag(propertyid, username, tag)
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

@app.route('/required_tax_tags/', defaults={'propertyid': None},  methods=['POST', 'GET'])
@app.route('/required_tax_tags/<propertyid>', methods=['POST'])
def required_tax_tags(propertyid):
    result = None
    if request.method == 'POST':
        username = request.json['username']
        result = astor_tags.get_required_tax_tags(propertyid, username)
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


@app.route('/access_tax_properties/<username>', methods=['GET'])
def access_tax_properties(username):
    result = None
    if request.method == 'GET':
        result = astor_tags.get_access_tax_properties(username)
        pass
    return result


@app.route('/add_access_tax_tag/', methods=['POST'])
def add_access_tax_tag():
    result = None
    if request.method == 'POST':
        username = request.json.get('username')
        propertyid = request.json.get('propertyid')
        result = astor_tags.add_access_tax_tag(propertyid, username)
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


@app.route('/address_url_match/<addr_url>')
def address_url_match(addr_url):
    result = get_address_url_match(addr_url)
    return result


@app.route('/calculated_tax/<bbl>/<year>')
def calculated_tax(bbl, year=None):
    result = get_calculated_tax(bbl, year)
    return result

# stripe related


@app.route('/add_user/', methods=['POST'])
def add_user():
    result = None
    if request.method == 'POST':
        username = request.json.get('username')
        email = request.json.get('email')
        stripe_id = request.json.get('stripeid')
        tos_checked = request.json.get('toschecked')
        privacy_policy_checked = request.json.get('privacypolicychecked')
        result = astor_users.add_user(username, email, stripe_id, tos_checked, privacy_policy_checked)
    return result


@app.route('/get_user_data/<email>')
def get_user_data(email):
    result = astor_users.get_user_data(email)
    return result


@app.route('/remove_url/<email>')
def remove_url(email):
    result = astor_users.remove_url(email)
    return result


@app.route('/add_purchase/', methods=['POST'])
def add_purchase():
    result = None
    if request.method == 'POST':
        stripe_session_id = request.json.get('stripe_session_id')
        email = request.json.get('email')
        property_id = request.json.get('property_id')
        purchase_date = request.json.get('purchase_date')
        result = astor_purchases.add_purchase(stripe_session_id, email, property_id, purchase_date)
    return result


@app.route('/delete_purchase/<session_id>')
def delete_purchase(session_id):
    result = astor_purchases.delete_purchase(session_id)
    return result


@app.route('/confirm_purchase/<session_id>')
def confirm_purchase(session_id):
    result = astor_purchases.confirm_purchase(session_id)
    return result


@app.route('/get_purchases/<session_id>')
def get_purchases(session_id):
    result = astor_purchases.get_purchases(session_id)
    return result


@app.route('/get_purchases_by_email/<email>')
def get_purchases_by_email(email):
    result = astor_purchases.get_purchases_by_email(email)
    return result


# covid_related
@app.route('/covid_data/<country>')
def covid_data(country=None):
    result = get_covid_data(country)
    return result


@app.route('/covid_data/')
def all_covid_data():
    logging.debug("covid data");
    result = get_covid_data()
    return result


@app.route('/state_model/<state>', methods=["GET","POST"])
def state_model(state=None):

    if request.method == "GET":
        result = get_state_timeline(state)
    elif request.method == "POST":
        json = request.json
        result = get_state_timeline(state, json)
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
