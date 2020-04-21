# London Top 100 Restaurants
Nowadays, with the introduction of so many restaurants, one of the biggest questions before meeting someone -" Which place should 
we go? Is it worth it?" This application tries to give answer to these questions by using the granular information from Zomato API
and presenting it in way to let us choose the right one of our choice.This app makes calls to an external API hosted in https://developers.zomato.com/api/v2.1/ .

### Features

- REST-based service interface.
- Interaction with external REST services.
- Use of on an external Cloud database(cassandra db) for persisting information.
- Support for cloud scalability, deployment in a container environment.
- Cloud security awareness by running my flask application over HTTPS Using self signed certificate.
- Request followup orchestration using HATEOAS.

### Services

#### External API

`1. GET @app.route('/usr/categories')` <br />
 Gets the categories of restaurants from the External API.  
 
`2. GET @app.route('/usr/collections')` <br />
Gets the collections of restaurants from the External API.  

`3. GET @app.route('/usr/cuisines'')` <br />
Gets the list of cuisines from the External API.

#### REST-based Service Interface
`1. GET @app.route('/usr/aggregates')` <br />
Extracts the Top 100 London restaurant details from Cassandra DB

`2. POST @app.route('/admin/citiesadd')` <br />
Adds the new city into the Cassandra DB  <br />
```curl -i -k -H "Content-Type: application/json" -X POST -d '{"id":720,"name":"Wakanda","country_name":"Gumbacha"}'    https://0.0.0.0:443/admin/citiesadd```

`3. PUT @app.route('/admin/citiesupd/<name>)` <br />
Updates the existing city in the Cassandra DB <br />
```curl -i -k -H "Content-Type: application/json" -X PUT -d '{"id":345,"country_name":"Baadumbe"}' &https://0.0.0.0:443/admin/citiesupd/Wakanda```

`4. DELETE @app.route('/admin/citiesdel/<name>')` <br />
Delete the existing city from the Cassandra DB <br />
 ```curl -k -X DELETE https://0.0.0.0:443/admin/citiesdel/Wakanda```




