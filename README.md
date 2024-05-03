<a href="https://scan.coverity.com/projects/vahshipanda-server">
  <img alt="Coverity Scan Build Status"
       src="https://scan.coverity.com/projects/29527/badge.svg"/>
</a>
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
3. browse api doc via http://vahshipanda-api:8080/docs
4. reload the backend services:
   ```bash
   uvicorn app:app --reload
   ```

if anything else changed (except py script), you may need to rebuild the image by using the following command:
```bash
# rebuild the docker images
docker compose build --no-cache

# run the servies
docker compose up -d
```

# Test
1. Test with curl: 
   ```bash
    curl http://vahshipanda-api:8080/api/v1/greet/1

    # obtain token
    curl -X 'POST' \
    'http://vahshipanda-api:8080/token' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'grant_type=&username=johndoe&password=secret&scope=&client_id=&client_secret='

    # interact with server
    curl -X 'GET' \
    'http://vahshipanda-api:8080/users/me' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer johndoe'

   ```

2. to use the pytest, please use the following command: 
   ```bash
   pytest -v -s
   ```