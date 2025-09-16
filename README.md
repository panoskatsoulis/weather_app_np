### How to run fron uploaded container

Download the docker and run it in the background, then open 2 terminals using the third command.
(you may build the container from the build file, assuming that there is some ubuntu image available locally
`sudo docker build -t weather_app_np .`)
```
sudo docker pull ghcr.io/panoskatsoulis/weather_app_np:v1
sudo docker run -dit weather_app_np:latest bash
sudo docker ps ## get the CONTAINER ID
sudo docker exec -it <CONTAINER ID> bash
```

From inside the container, run the backend in one terminal
```
cd /weather_app_np
python backend/app_backend.py --debug
```

From inside the container, run clients in the other terminal (`ctrl-C` to kill)
```
cd /weather_app_np
emacs station_sim/sim-config.ini ## configure the clients, interval in sec
python3 station_sim/client.py
```

To add more clients, open `station_sim/sim-config.ini` and add likes to [INSTANCES] and [TOKENS]<br>
New tokens should be generated and added to the sqlite file
*DON'T add too many, the backend is written in a syncronous way* (or at least change the interval in `station_sim/sim-config.ini`)
```
openssl rand -base64 12 ## new tokens
sqlite3 backend.db "insert into stations (token) values ('31ATs5WxJcIzWVYx')" ## insert the token
sqlite3 backend.db 'select * from stations' ## check it
```
