from flask import Flask, escape, request, abort
import logging
from astor_real_estate import *
from astor_search import *
import astor_real_estate
import astor_tags
import astor_users
import astor_purchases
import astor_search
import astor_tax_protest
import datetime
import json

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

# app = Flask(__name__)
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


# broker product related


@app.route('/broker_query_neighborhoods/')
def broker_query_neighborhoods():
    result = get_broker_query_neighborhoods()
    return result


# tax related


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


@app.route('/tax_tags/', defaults={'propertyid': None}, methods=['POST', 'GET'])
@app.route('/tax_tags/<propertyid>', methods=['POST'])
def tax_tags(propertyid):
    result = None
    if request.method == 'POST':
        username = request.json['username']
        result = astor_tags.get_tax_tags(propertyid, username)
        pass
    return result


@app.route('/required_tax_tags/', defaults={'propertyid': None}, methods=['POST', 'GET'])
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


@app.route('/property_tags/', defaults={'propertyid': None}, methods=['POST', 'GET'])
@app.route('/property_tags/<propertyid>', methods=['POST', 'GET'])
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

@app.route('/shortcut_app_forward/<addr_url>')
def shortcut_app_forward(addr_url):
    result = address_app_dest(addr_url)
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
        full_name = request.json.get('full_name')
        avatar = request.json.get('avatar')
        result = astor_users.add_user(username, email, stripe_id, tos_checked, privacy_policy_checked, full_name, avatar)
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


@app.route('/confirm_purchase/<session_id>', methods=["GET"])
def confirm_purchase(session_id):
    result = astor_purchases.confirm_purchase(session_id)
    return result


@app.route('/confirm_purchase/', methods=["POST"])
def confirm_individual_purchase():
    result = None
    if request.method == 'POST':
        email = request.json.get('email')
        property_id = request.json.get('property_id')
        result = astor_purchases.confirm_individual_purchase(email, property_id)
    return result


@app.route('/get_purchases/<session_id>')
def get_purchases(session_id):
    result = astor_purchases.get_purchases(session_id)
    return result


@app.route('/get_purchases_by_email/<email>')
def get_purchases_by_email(email):
    result = astor_purchases.get_purchases_by_email(email)
    return result


@app.route('/get_selected_comparables/<bbl>')
def get_selected_comparables(bbl):
    result = astor_real_estate.get_selected_comparables(bbl)
    return result


@app.route('/get_user_selected_comparables/<bbl>/<username>')
def get_user_selected_comparables(bbl, username):
    result = astor_real_estate.get_user_selected_comparables(bbl, username)
    return result


@app.route('/delete_user_selected_comparables/<bbl>/<username>')
def delete_user_selected_comparables(bbl, username):
    result = astor_real_estate.delete_user_selected_comparables(bbl, username)
    return result


@app.route('/set_user_selected_comparables/<bbl>/<username>', methods=["POST"])
def set_user_selected_comparables(bbl, username):
    result = None
    if request.method == 'POST':
        comparables = request.json.get('comparables')
        result = astor_real_estate.set_user_selected_comparables(bbl, username, comparables)
    return result


@app.route('/log_search/', methods=['POST'])
def log_search():
    result = None
    if request.method == 'POST':
        ip_addr = request.json.get('ip_addr')
        username = request.json.get('username')
        search_string = request.json.get('search_string')
        milliseconds = request.json.get('timestamp')
        timestamp = datetime.datetime.fromtimestamp(milliseconds / 1000.0)
        result = astor_search.log_search(ip_addr, username, search_string, timestamp)
    return result


@app.route('/save_tax_protest/', methods=['POST'])
def save_tax_protest():
    result = None
    if request.method == 'POST':
        result = astor_tax_protest.save_protest(request.json)
    return json.dumps([result])


@app.route('/get_tax_protest/<bbl>/<email>')
def get_tax_protest(bbl=None, email=None):
    result = []
    result = astor_tax_protest.get_tax_protest(bbl, email)
    return json.dumps(result)


@app.route('/get_management_company/<email>')
def get_management_company(email):
    result = astor_users.get_management_company(email)
    return result


@app.route('/get_data_dictionary/')
def get_data_dictionary():
    result = astor_real_estate.get_Data_Dict()
    return result

@app.route('/billcheck/<bbl>/<year>')
def get_billcheck(bbl, year=2022):
    result = astor_real_estate.billcheck(bbl, int(year))

    return result

@app.route('/transactions/<bbl>/<year>')
@app.route('/transactions/<bbl>/')
def get_transactions(bbl, year=None):
    if year is not None:
        year = int(year)
    result = astor_real_estate.transactions(bbl, year)

    return result


@app.route('/get_lawyer/<bbl>/')
def get_lawyer(bbl):
    result = astor_real_estate.get_lawyer(bbl)
    return result


@app.route('/authorized_new_user/<email>')
def authorized_new_user(email):
    result = astor_users.authorized_new_user(email)
    return result


@app.route('/get_signup_urls/')
def get_signup_urls():
    result = astor_users.get_signup_urls()
    return result


@app.route('/get_auth_properties/<email>')
def get_auth_properties(email):
    result = astor_tags.get_auth_properties(email)
    return result


@app.route('/get_historical_taxes/<bbl>')
def get_historical_taxes(bbl):
    result = astor_real_estate.get_historical_taxes(bbl)
    return result


@app.route('/get_energy_grade/<bbl>')
def get_energy_grade(bbl):
    result = astor_real_estate.get_energy_grade(bbl)
    return result


@app.route('/get_violations/<bbl>')
def get_violations(bbl):
    result = astor_real_estate.get_violations(bbl)
    return result


@app.route('/is_authorized/<user>/<bbl>')
def is_authorized(user, bbl):
    result = astor_real_estate.is_violations(user, bbl)
    return result


@app.route('/get_contact_info/<bbl>')
def get_contact_info(bbl):
    result = astor_real_estate.get_contact_info(bbl)
    return result


@app.route('/set_management_company_contact_info/<bbl>', methods=['POST'])
def set_management_company_contact_info(bbl):
    if request.method == 'POST':
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        result = astor_real_estate.set_management_company_contact_info(bbl, name, email, phone)
    return result


@app.route('/set_board_president_contact_info/<bbl>', methods=['POST'])
def set_board_president_contact_info(bbl):
    if request.method == 'POST':
        name = request.json['name']
        email = request.json['email']
        phone = request.json['phone']
        result = astor_real_estate.set_board_president_contact_info(bbl, name, email, phone)
    return result


@app.route('/get_demo_info/<demo_name>')
def get_demo_info(demo_name):
    result = astor_users.get_demo_info(demo_name)
    return result


@app.route('/check_tos/<email>')
def check_tos(email):
    result = astor_users.check_tos(email)
    return result


@app.route('/check_privacy_policy/<email>')
def check_privacy_policy(email):
    result = astor_users.check_privacy_policy(email)
    return result


@app.route('/exemption/<bbl>')
def exemption(bbl):
    result = astor_real_estate.get_exemption(bbl)
    return result


@app.route('/caprate/<bbl>')
def get_caprate(bbl):
    result = astor_real_estate.get_caprate(bbl)
    return result


@app.route('/submit_email', methods=['POST'])
def submit_email():
    status = 500
    result = "ERROR"
    if request.method == 'POST':
        email = request.json['email']
        referer = request.json['referer']
        result = astor_users.submit_email(email, referer)
        status = 200
        if result != 'SUCCESS':
            abort(500)
    return result, status
