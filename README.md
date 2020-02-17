### Pi Exchange Test
Customer Management for Telephone Company


**Technology Stack**

* Python, Flask for API backend
* SQLite for db

**Storage Design**

SQL database with Customer table with (id, name, phone_number) with an index on phone_number. Because the application is heavily dependent on searching through customers by phone_number, an index is used to improve performance.

For speed and development of challenge, sqlite was used but in real world suitable a more production SQL database like PostgreSQL would be used.

To handle the hundreds of millions of phone numbers, standard vertical and horizontal db scaling can be used. Also trading off memory for further performance, we could design the Customer table with (id, name, phone_number, prefix1 .. prefix10) and have indexes on phone_number and prefix 1-10. This will allow direct search depending on the prefix search.

**API**

```
GET /customers?prefix=123
```

Get customers resource with optional prefix search

```
POST /customers
```

Create customer resource with (name, phone_number) key value pairs in form-data

**Run Instructions**

Build sqlite db with 10k records ~ 60 seconds
```
python db_init.py
```

Docker build, run and stop commands
```
docker image build -t pi_exchange:1.0 .

docker container run --publish 8000:5000 --detach --name pe pi_exchange:1.0

docker stop pe
```


**Test**

GET, localhost:8000/customers?prefix=123

POST, localhost:8000/customers?prefix=123, form-data: {name: "John Smith", phone_number: "12345678901"}

Can use Postman for this
