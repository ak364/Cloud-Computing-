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

`1. GET @app.route('/usr/categories')`
 Gets the categories of restaurants from the External API.
`2. GET @app.route('/usr/collections')`
`3. GET @app.route('/usr/cuisines'')`

#### REST-based Service Interface
`1. GET @app.route('/usr/aggregates')`
`2. POST @app.route('/admin/citiesadd')`
`3. PUT @app.route('/admin/citiesupd/<name>)`
`4. DELETE @app.route('/admin/citiesdel/<name>')`



