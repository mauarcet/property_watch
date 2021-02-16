# Property Watch

This API provides a service that allows the registration properties listed on M3.
It's constructed under the Django Rest Framework.

## Installation

This project comes with a Docker recipe. `docker-compose` and `Docker` are required for the installation.

Clone the project

```
git clone https://github.com/mauarcet/property_watch.git
cd property_watch
```

From the command line run:

```
docker-compose up
```

## Tests

In order to run the test suite kill the server with: `Ctrl+c`.

From the command line run:

```
docker-compose run --service-ports web python property_watch/manage.py test api
```

## Usage

### Seed database

The main feature of the project is the seed. This process scraps M3 main listing page and brings the required number of properties

The query param `limit` sets the number of properties to scrap for.

```
curl --location --request POST 'http://127.0.0.1:8000/seed/?limit=1'
```

### GET Properties

All the seeded properties can be retrieved via API by the endpoint `properties/`.

The query param `limit` sets the number of properties to retrieve.

```
curl --location --request GET 'http://127.0.0.1:8000/properties/?limit=1'
```
