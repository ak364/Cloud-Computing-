from flask import Flask, jsonify, json, render_template, request, abort
import requests
import os
from cassandra.cluster import Cluster
from dotenv import load_dotenv

cluster = Cluster(contact_points=['172.17.0.2'], port=9042)
#cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
session = cluster.connect()
load_dotenv()
API_KEY = os.getenv('PROJECT_API_KEY')

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('index.html')


# External API call
# Summary information : Includes country stats and global stats
@app.route('/usr/categories', methods=['GET'])
def zomato_cat():
    url = "https://developers.zomato.com/api/v2.1/categories"
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": API_KEY}
    payload = {}
    response = requests.request("GET", url, headers=header, data=payload)
    return response.json()


@app.route('/usr/collections', methods=['GET'])
def zomato_colls():
    url = "https://developers.zomato.com/api/v2.1/collections?city_id=61"
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": API_KEY}
    payload = {}
    response = requests.request("GET", url, headers=header, data=payload)
    return response.json()


@app.route('/usr/cuisines', methods=['GET'])
def zomato_cuis():
    url = "https://developers.zomato.com/api/v2.1/cuisines?city_id=61"
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": API_KEY}
    payload = {}
    response = requests.request("GET", url, headers=header, data=payload)
    return response.json()


# Aggregate stats using Cassandra db # code extract_api_dat.py>fix_json.py
@app.route('/usr/aggregates', methods=['GET'])
def summary_det():
    rows = session.execute(""" SELECT * FROM zomato.summary """)
    result = []
    for r in rows:
        result.append(
            {
                "Name": r.name,
                "Agg Rating": r.aggregate_rating,
                "Cost for two": r.average_cost_for_two,
                "City": r.city,
                "ID": r.id,
                "Cuisines": r.cuisines,
                "Locality": r.locality,
                "Rating": r.rating_text,
                "Votes": r.votes
            })
    return render_template("summary.html", data=result)


@app.route('/admin/citiesadd', methods=['POST'])
def add_city():
    if not request.json or not 'id' in request.json \
            or not 'name' in request.json \
            or not 'country_name' in request.json:
        abort(400, 'Bad request.Check your parameters')

    id_name = request.json['id']
    name = request.json['name']
    country_name = request.json['country_name']

    result = session.execute("""select count(*) from zomato.cities where name='{}'ALLOW FILTERING""".format(name))
    if result.was_applied == 0:
        queryAddCity = """insert into zomato.cities(id, name, country_name) 
        values ({},'{}','{}')""".format(id_name, name, country_name)
        session.execute(queryAddCity)
        return "Success", 201

    else:
        abort(406, description="The city already exist in the database")

@app.route('/admin/citiesupd/<name>', methods=['PUT'])
def upd_city(name):
    if not request.json:
        abort(400, 'Bad Request. Check your parameters')

    id_num= request.json['id']
    city = name
    country_name = request.json['country_name']

    results=session.execute("""SELECT * FROM ZOMATO.CITIES WHERE NAME = '{}'ALLOW FILTERING""".format(name))
    if len(results.current_rows)==0:
        abort(404, description="No such city or check country spellings. name:{}".format(name))
    else:
        queryUpdateCity="""UPDATE ZOMATO.CITIES SET id={},country_name='{}' WHERE name='{}'""".format(id_num, country_name, city)
        session.execute(queryUpdateCity)
        return "Success", 201

@app.route('/admin/citiesdel/<name>', methods=['DELETE'])
def del_city(name):
    results = session.execute("""SELECT * FROM ZOMATO.CITIES WHERE NAME = '{}'ALLOW FILTERING""".format(name))
    if len(results.current_rows) == 0:
        abort(404, description="{} does not exist.".format(name))
    else:
        queryDelCity="""DELETE FROM ZOMATO.CITIES where name='{}'""".format(name)
        session.execute(queryDelCity)
        return "Success", 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))
    #app.run()
