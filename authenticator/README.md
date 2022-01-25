# Django RESTfull Authentication API Application

# REST API

The REST API to the app is described below.

# User model endpoints

## Get list of Users

### Request

`GET /auth/users`

    'Accept: application/json' http://localhost:8000/auth/users

### Response

    HTTP/1.1 200 OK
    Date: Mon, 17 Jan 2022 12:00:35 GMT
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 717

```json
    [
	    {
		    "id": 1,
		    "email": "test@gmail.com",
		    "first_name": "John",
		    "last_name": "Wick",
		    "role": {
			    "id": 1,
			    "name": "User",
			    "description": "Common User Role"
		    },
		    "created": "2022-01-19"
	    },
	    {
		    "id": 2,
		    "email": "spidey@gmail.com",
		    "first_name": "Peter",
		    "last_name": "Parker",
		    "role": {
		    	"id": 1,
		    	"name": "User",
		    	"description": "Common User Role"
	    	},
		    "created": "2022-01-24"
	    }
    ]
```

## Create a new User

### Request

`POST /auth/users`

    'Accept: application/json' http://localhost:8000/auth/users

```json
    {
	    "email": "quiny@gmail.com",
	    "first_name": "Harley",
	    "last_name": "Quinn",
	    "password": "qwerty"
    }
```

### Response

    HTTP/1.1 201 Created
    Date: Mon, 17 Jan 2022 09:31:18 GMT
    Status: 201 Created
    Content-Type: application/json
    Content-Length: 178

```json
    {
	    "id": 4,
	    "email": "quiny@gmail.com",
	    "first_name": "Harley",
	    "last_name": "Quinn",
	    "role": {
		    "id": 1,
		    "name": "User",
		    "description": "Common User Role"
	    },
	    "created": "2022-01-17"
    }
```

## Get a specific User

### Request

`GET /auth/user/:email`

    'Accept: application/json' http://localhost:8000/auth/users/test@gmail.com

### Response

    HTTP/1.1 200 OK
    Date: Mon, 17 Jan 2022 09:01:27 GMT
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 174

```json
    {
	    "id": 1,
	    "email": "test@gmail.com",
	    "first_name": "John",
	    "last_name": "Wick",
	    "role": {
		    "id": 1,
		    "name": "User",
		    "description": "Common User Role"
	    },
	    "created": "2022-01-17"
    }
```

## Get a non-existent User

### Request

`GET /auth/users/:email`

    'Accept: application/json' http://localhost:8000/auth/users/qwerty

### Response

    HTTP/1.1 404 Not Found
    Date: Mon, 17 Feb 2022 12:36:30 GMT
    Status: 404 Not Found
    Content-Type: application/json
    Content-Length: 0

## Edit a User

### Request

`PUT /auth/user/:email`

    'Accept: application/json' http://localhost:8000/auth/user/quin@gmail.com

```json
    {
	    "email": "not.quiny@gmail.com",
	    "first_name": "Margot",
	    "last_name": "Robbie",
	    "role": "2",
	    "password":
	    {
		    "new": "asdzxc",
		    "confirm": "asdzxc",
		    "old": "qwerty"
	    }
    }
```

### Response

    HTTP/1.1 200 OK
    Date: Mon, 17 Feb 2022 12:36:31 GMT
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 185

```json
    {
	    "id": 4,
	    "email": "not.quiny@gmail.com",
	    "first_name": "Harley",
	    "last_name": "Quinn",
	    "role": {
		    "id": 2,
		    "name": "Admin",
		    "description": "Administrator Role"
	    },
	    "created": "2022-01-24"
    }
```

## Delete a User

### Request

`DELETE /auth/user/:email`

    application/json' http://localhost:8000/auth/user/test@gmail.com/

### Response

    HTTP/1.1 204 No Content
    Date: Mon, 17 Feb 2022 12:36:32 GMT
    Status: 204 No Content


## Try to delete same User again

### Request

`DELETE /auth/user/:email`

    'Accept: application/json' http://localhost:8000/auth/user/test@gmail.com/

### Response

    HTTP/1.1 404 Not Found
    Date: Mon, 17 Feb 2022 12:36:32 GMT
    Status: 404 Not Found
    Content-Type: application/json
    Content-Length: 0

## Get deleted User

### Request

`GET /auth/user/:email`

    'Accept: application/json' http://localhost:8000/auth/user/test@gmail.com

### Response

    HTTP/1.1 404 Not Found
    Date: Mon, 17 Feb 2022 12:36:33 GMT
    Status: 404 Not Found
    Content-Type: application/json
    Content-Length: 0

# Role model enpoints

## Get list of Roles

### Request

`GET /auth/roles`

    'Accept: application/json' http://localhost:8000/auth/roles

### Response

    HTTP/1.1 200 OK
    Date: Mon, 17 Jan 2022 12:49:56 GMT
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 213

```json
    [
	    {
		    "model": "authenticator.role",
		    "pk": 1,
		    "fields": {
		    	"name": "User",
			    "description": "Common User Role"
		    }
	    },
	    {
		    "model": "authenticator.role",
		    "pk": 2,
		    "fields": {
		    	"name": "Admin",
			    "description": "Administrator Role"
	    	}
	    }
    ]
```

## Create a new Role

### Request

`POST /auth/roles`

    'Accept: application/json' http://localhost:8000/auth/roles

```json
    {
	    "role": "Manager",
	    "desc": "Manager Role"
    }
```

### Response

    HTTP/1.1 200 OK
    Date: Mon, 17 Jan 2022 09:03:56 GMT
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 59

```json
    {
	    "id": 3,
	    "name": "Manager",
	    "description": "Manager Role"
    }
```

## Get a specific Role

### Request

`GET /auth/roles/:id`

    'Accept: application/json' http://localhost:8000/auth/roles/3

### Response

    HTTP/1.1 200 OK
    Date: Mon, 17 Jan 2022 13:00:05 GMT
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 59

```json
    {
	    "id": 3,
	    "name": "Manager",
	    "description": "Manager Role"
    }
```

## Get a non-existent Role

### Request

`GET /auth/roles/:id`

    'Accept: application/json' http://localhost:8000/auth/roles/4

### Response

    HTTP/1.1 404 Not Found
    Date: Mon, 17 Jan 2022 13:02:25 GMT
    Status: 404 Not Found
    Content-Type: application/json
    Content-Length: 0

## Edit Role

### Request

`PUT /auth/roles/:id`

    'Accept: application/json' http://localhost:8000/auth/roles/3

```json
    {
	    "name": "Redactor",
	    "description": "Retactor role"
    }
```

### Response

    HTTP/1.1 200 OK
    Date: Mon, 17 Jan 2022 09:07:56 GMT
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 61

```json
    {
	    "id": 3,
	    "name": "Redactor",
	    "description": "Retactor role"
    }
```

## Delete a Role

### Request

`DELETE /auth/roles/:id`

    'Accept: application/json' http://localhost:8000/auth/roles/3

### Response

    HTTP/1.1 204 No Content
    Date: Mon, 17 Feb 2022 13:20:05 GMT
    Status: 204 No Content

## Delete same Role again

### Request

`DELETE /auth/roles/:id`

    'Accept: application/json' http://localhost:8000/auth/roles/3

### Response

    HTTP/1.1 404 Not Found
    Date: Mon, 17 Feb 2022 13:20:55 GMT
    Status: 204 Not Found
    Content-Type: application/json
    Content-Length: 0


# Token model endpoints

## Generate new JWT via refresh token

### Request

`POST /auth/token`

    'Accept: application/json' http://localhost:8000/auth/token

```json
    {
	    "email": "test@gmail.com",
	    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDM2NDI4NDUsImlhdCI6MTY0MzAzODA0NSwidXNlciI6InRlc3RAZ21haWwuY29tIn0.BOtruo6c1EmEcHRwN7ekrn0OcteHSj1IZ3xmDQyMj_w"
    }
```

### Response


    HTTP/1.1 200 OK
    Date: Mon, 17 Jan 2022 12:53:56 GMT
    Status: 200 OK
    Content-Type: application/json
    Content-Length: 361

```json
    {
	    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDUyNzk2MDUsImlhdCI6MTY0MzExOTYwNSwidXNlciI6InRlc3RAZ21haWwuY29tIn0.CeRmncPIgz472rEystTulewn3ksA4EyR-h0MAUsEMaw",
	    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDM3MjQ0MDUsImlhdCI6MTY0MzExOTYwNSwidXNlciI6InRlc3RAZ21haWwuY29tIn0.OHkmaIk0nEFbXnCPFYu92P6sBAj7_-Ybk0kmgoSqGE0"
    }
```


