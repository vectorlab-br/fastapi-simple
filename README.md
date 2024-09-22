# fastapi-simple
 FastAPI simple app

# To build
docker build . --tag vectorlab/fastapi-test-app --no-cache

# To publish to docker.com
docker push vectorlab/fastapi-test-app

# To run
docker run -d -p 5000:5000 vectorlab/fastapi-test-app

# To run with compose in watch mode
docker compose watch