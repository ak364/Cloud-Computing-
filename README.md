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
```
curl -i -k -H "Content-Type: application/json" -X POST -d '{"id":720,"name":"Wakanda","country_name":"Gumbacha"}'    https://0.0.0.0:443/admin/citiesadd
```

`3. PUT @app.route('/admin/citiesupd/<name>)` <br />
Updates the existing city in the Cassandra DB <br />
```
curl -i -k -H "Content-Type: application/json" -X PUT -d '{"id":345,"country_name":"Baadumbe"}' &https://0.0.0.0:443/admin/citiesupd/Wakanda
```

`4. DELETE @app.route('/admin/citiesdel/<name>')` <br />
Delete the existing city from the Cassandra DB <br />
 ```
 curl -k -X DELETE https://0.0.0.0:443/admin/citiesdel/Wakanda
 ```
### Deployment

1.Inital Steps
```
sudo apt update
sudo apt install docker.io
sudo docker pull cassandra:latest
```

2.Run cassandra in a Docker container and expose port 9042:
```
sudo docker run --name cassandra-prod -p 9042:9042 -d cassandra
```

3.Download csv file with aggregates
```
wget https://raw.githubusercontent.com/ak364/Cloud-Computing-/master/final_db_input.csv
```

4.Moving the file to Cassandra home path
```
sudo docker cp final_db_input.csv cassandra-prod:/home/final_db_input.csv
```

5.Access the cassandra container in iterative mode
```
sudo docker exec -it cassandra-prod cqlsh
```

6.Create a keyspace inside Cassandra for the Zomato restaurant DB
```
cqlsh> CREATE KEYSPACE zomato WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
```

7.Create the database table for the aggregates
```
cqlsh> CREATE TABLE zomato.summary (
       name text PRIMARY KEY,
       aggregate_rating float,
       average_cost_for_two int,
       city text,
       cuisines text,
       id int,
       locality text,
       rating_text text,
       votes int
      );
```
8.Create the database table for the cities
```
cqlsh> CREATE TABLE zomato.cities (
       name text PRIMARY KEY,
       country_name text,
       id int);
```

9.Loading the above aggregates csv file into Cassandra DB.
```
cqlsh>COPY zomato.summary(id,name,locality,city,cuisines,average_cost_for_two,aggregate_rating,rating_text,votes)
      FROM '/home/final_db_input.csv'
      WITH HEADER=TRUE;
 ```

### Security
This app is served over HTTPS using self-signed certificate. The keys were obtained using below command in project directory.
```
$ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

### HATEOAS (Hypermedia as the Engine of Application State)
It is a constraint of the REST application architecture that keeps the RESTful style architecture unique from most other network application architectures. The term “hypermedia” refers to any content that contains links to other forms of media such as images, movies, and text.

This architectural style lets you use hypermedia links in the response contents so that the client can dynamically navigate to the appropriate resource by traversing the hypermedia links. This is conceptually the same as a web user navigating through web pages by clicking the appropriate hyperlinks in order to achieve a final goal.

When you try to make a get request like Based on the id, It queries the database and creates a dynamic JSON.

### Execution
```
cd mini_project/
sudo docker build . --tag=miniproject:v1
sudo docker run -dp 443:443 miniproject:v1
```

Remember to add https infront of the AWS public url.











