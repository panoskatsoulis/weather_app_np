### How to run from uploaded container

Download the docker and run it in the background, then open 2 terminals using the fourth command below.
(you also may build the container from the build file, assuming that there is some ubuntu image available locally
<br>`sudo docker build -t weather_app_np .`)
```
sudo docker pull ghcr.io/panoskatsoulis/weather_app_np:v1.1
sudo docker run -dit weather_app_np:latest bash
sudo docker ps ## get the CONTAINER ID
sudo docker exec -it <CONTAINER ID> bash
```

From inside the container, run the backend in one terminal
```
cd /weather_app_np
. venv/bin/activate
python backend/app_backend.py --debug
```

From inside the container, run clients in the other terminal (`ctrl-C` to kill)
```
cd /weather_app_np
emacs station_sim/sim-config.ini ## configure the clients, interval in sec
. venv/bin/activate
python3 station_sim/client.py
```

To add more clients, open `station_sim/sim-config.ini` and add likes to [INSTANCES] and [TOKENS]<br>
New tokens should be generated and added to the sqlite file.
***DON'T add too many, the backend is written in a syncronous way*** (or at least change the interval in `station_sim/sim-config.ini`)
```
openssl rand -base64 12 ## new tokens
sqlite3 backend.db "insert into stations (token) values ('31ATs5WxJcIzWVYx')" ## insert the token
sqlite3 backend.db 'select * from stations' ## check it
```

One should initiate the database if decides not to use the prepared sqlite file `backend/backend.db`.
Once initiated, tokens should be registered to the stations table like above.
```
cd /weather_app_np
python backend/app_backend.py --init ## creates new sqlite file
```
