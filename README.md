# VahshiPanda-Server
It's a backend code for VahshiPanda App powered by fastapi framework.

# Usage

1. Run services in background using: 
    ```bash
    docker compose -f compose_db.yaml up -d
    docker compose up -d
    ```
2. Check the services
    ```bash
    docker compose ps
    ```
3. browse api doc via http://127.0.0.1:8080/docs

# Test
1. Test with curl: 
   ```bash
    curl http://127.0.0.1:8080/api/v1/greet/1

    # obtain token
    curl -X 'POST' \
    'http://127.0.0.1:8080/token' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'grant_type=&username=johndoe&password=secret&scope=&client_id=&client_secret='

    # interact with server
    curl -X 'GET' \
    'http://127.0.0.1:8080/users/me' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer johndoe'

   ```