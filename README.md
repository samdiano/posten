# Posten

Posten allows users to create, read, update, and delete users and posts. Users can also like and unlike any post.

## Getting Started
1. Clone the repository.
```bash
git clone git@github.com:samdiano/posten.git
```

2. Create a virtual environment and activate it.
```bash
python3 -m virtualenv env

source env/bin/activate
```

3. Install the requirements.
```bash
pip install -r requirements.txt
```

4. migrate the database.
```bash
python manage.py makemigrations && python manage.py migrate
```

5. Create a superuser.
```bash
python manage.py createsuperuser --email john@example.com --username john
```

6. Run the server.
```bash
python manage.py runserver
```

## Usage
### Authentication
To authenticate, obtain an access token by sending a POST request to the /login endpoint with a JSON payload containing a `username` and `password` field. The server will respond with a JSON object containing the access token.

Include the access token in the `Authorization` header of subsequent requests as follows:

```bash 
GET /posts 
Authorization: Bearer your_access_token
```

## Endpoints
### Posts
- GET /api/posts: Get a list of all posts.
- POST /api/posts: Create a new post.
- GET /api/posts/:id Get a post by ID.
- PUT /api/posts/:id Update a post by ID.
- DELETE /api/posts/:id Delete a post by ID.
- POST /api/posts/:id/like: Like a post by ID.
- POST /api/posts/:id/unlike: Unlike a post by ID.

### Auth
- POST /api/login: Login a user.
- POST /api/signup: Signup a user.

### Users
- GET /api/users: Get a list of all users.
- POST /api/users/create: Create a new user.
- GET /api/users/:id Get a user by ID.
- PUT /api/users/:id Update a user by ID.
- DELETE /api/users/:id Delete a user by ID.


## Testing
To run the tests, use the following command:
```bash
python manage.py test
```

## Swagger Documentation
The Swagger documentation for the API can be accessed by running the server and navigating to `/api/docs`. This provides an interactive documentation for all the endpoints

