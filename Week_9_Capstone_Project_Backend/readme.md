
# Pet Store E-commerce Backend

This project is a Flask based API for a pet store platform. It provides functionalities for user authentication, product management, a shopping cart, and order processing. The application uses PostgreSQL for data bases, Redis for caching, and RS256 JWTs for authentication.



## Prerequisites

Before you begin, make sure you have the following installed on your system:

1. Python 3.10 or greater

2. OpenSSL (for generating security keys)



##  Setup Instructions

Follow these steps to get the development environment up and running.



### 1. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

```txt
Flask
SQLAlchemy
psycopg2-binary
jwt
redis
pytest
```

### 2. Set Up Database & Cache

For this, do the following steps:

1. Install PG manager and create a new DB. Save the access credentials. 

2. Then, create the schema "week_9_capstone_project". 

3. Once the DB is created and the credentials saved, open an acount with redis and create a free server. Save these credentials.

### 3. Configure Environment Variables

The application uses a .env file for configuration.

1.  Copy the example file .env.example to a new file named .env.


Your .env file should look like this:

```ini
# Postgres
DB_NAME="your_db_name"
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"
DB_HOST="localhost"

# Redis
REDIS_HOST="localhost"
REDIS_PORT="PORTHERE"
REDIS_USERNAME="USERNAMEHERE"
REDIS_PASSWORD="PASSWORDHERE"
CACHE_TTL="300"
```

### 4. Generate RSA Keys for JWT

The application uses the RS256 algorithm for signing JSON Web Tokens, which requires a key pair.

1.  Create a directory named keys in the project root.
```bash
mkdir keys
```
2.  Generate the private key.
```bash
openssl genpkey -algorithm RSA -out keys/private.pem -pkeyopt rsa_keygen_bits:2048
```
3.  Extract the public key from the private key.
```bash
openssl rsa -pubout -in keys/private.pem -out keys/public.pem
```
These keys are used by the JWT_Manager to sign and verify tokens.



## Running the Application

Once the setup is complete, you can run the Flask application. The server will start on `localhost:5000`.

```bash
python main.py
```
The first time you run the application, the necessary database tables will be created automatically. The roles table will also be seeded with user and admin roles.



## Running Tests

The project includes a slew of tests located in the `/tests` directory. To run the tests, use pytest.

```bash
pytest
```
The test programs uses mocked repositories to test the API endpoints without needing a live database connection.



## API Endpoints

Here is a summary of the available API endpoints. A valid JWT token is required for all endpoints under `/api`. These tables were created with tablesgenerator.com/markdown_tables.

### Authentication

| Method | Endpoint          | Description                                    |
| :----- | :---------------- | :--------------------------------------------- |
| `POST` | `/auth/register`  | Registers a new user.                |
| `POST` | `/auth/login`     | Authenticates a user and returns a JWT. |

### Products

| Method   | Endpoint                | Access | Description                                     |
| :------- | :---------------------- | :----- | :---------------------------------------------- |
| `POST`   | `/api/products`         | Admin  | Creates a new product.                |
| `GET`    | `/api/products`         | User   | Retrieves a list of all products.     |
| `GET`    | `/api/products/<id>`    | User   | Retrieves a single product by its ID. |
| `PUT`    | `/api/products/<id>`    | Admin  | Updates a product's details.          |
| `DELETE` | `/api/products/<id>`    | Admin  | Deletes a product.                    |

### Sales & Cart

| Method | Endpoint          | Access | Description                                |
| :----- | :---------------- | :----- | :----------------------------------------- |
| `GET`  | `/api/cart`       | User   | Views the items in the current active cart. |
| `POST` | `/api/cart/items` | User   | Adds an item to the cart.       |
| `POST` | `/api/checkout`   | User   | Processes the cart and creates an invoice. |
| `POST` | `/api/refunds`    | Admin  | Processes a refund for a product. |

 ```