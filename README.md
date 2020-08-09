# Transmission Connect

transmission-sonarr-radarrr-config hopes to automatically 
configure torrent clients to other PVR services 
such as sonarr and radarr within a cluster of docker containers
within their own networks automatically so that you dont need to everytime your download client goes turns on and off 

## Why
network variables such as the IP addresses change when constantly started and stopped in their containers, this script hopes to avoid you from constantly having to manually configure these variables. Networks such as Bridge in docker have their own independent networks, configuring them manually every time you need to switch on/off your client seems inefficient, instead this script will start your download client in your docker container and configure you PVR services to them. (must be configured at least once before)
![Docker Bridge Network](https://docs.docker.com/engine/tutorials/bridge2.png)

## Installation and Usage
tested on python 3.8.2
```
pip install -r requirements.txt
```

Configure your .env file
```
SONARRAPIKEY='r3q687b6gdcuswrb7i3qtbiirbsirr2'
SONARRHOST='localhost'
SONARRPORT='8989'
RADARRAPIKEY='csgbifr4tbwq9rq3xqwurynae7rwhn3'
RADARRHOST='localhost'
RADARRPORT='7878'
DOWNLOADCLIENT='transmission'
```
start script
```
python3 transmission-connect.py
```