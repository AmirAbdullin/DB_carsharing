docker build . -t carsharing:latest --network=host
docker run -it --env-file .env -p 80:80 carsharing:latest 