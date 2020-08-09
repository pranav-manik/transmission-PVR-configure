import docker
from sys import exit
import os
import requests
import json
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


try:
    client = docker.from_env()
    APIClient = docker.APIClient(base_url='unix://var/run/docker.sock')
    print('docker connected')
    containers = client.containers.list(all=True)
    transmission = client.containers.get(os.getenv("DOWNLOADCLIENT"))
    print(os.getenv("DOWNLOADCLIENT"), 'status:', transmission.status)

    # start up docker container for downloadclient
    
    if transmission.status != 'running':
        print(transmission)
        transmission.start()
    else:
        print('already on')
        # exit(0)
    started = False
    while (started == False):
        print('starting...')
        if (client.containers.get(os.getenv("DOWNLOADCLIENT")).status == 'running'):
            started = True

    # grab container info

    print(os.getenv("DOWNLOADCLIENT"), 'status:', client.containers.get(os.getenv("DOWNLOADCLIENT")).status)
    print('container:', client.containers.get(os.getenv("DOWNLOADCLIENT")))
    print('name:', transmission.name)
    print('id:', client.containers.get(os.getenv("DOWNLOADCLIENT")).id)
    transmissionIP = ''
    for currCont in APIClient.containers():
        if currCont['Names'][0] == '/' + os.getenv("DOWNLOADCLIENT"):
            transmissionIP = currCont['NetworkSettings']['Networks']['bridge']['IPAddress']
    print('IP Address:', transmissionIP, '\n')

    # config sonarr and radarr clients and connect to download clients
    sonarr = requests.get("http://" + os.getenv("SONARRHOST") + ":" + 
        os.getenv("SONARRPORT") +
        "/api/downloadclient?apikey="+
        os.getenv("SONARRAPIKEY"))
    print('sonarr GET request status:', sonarr.status_code)
    
    # grab client info and configure
    clientInfo = None
    for client in sonarr.json():
        if (str(client['name']) == str(os.getenv("DOWNLOADCLIENT"))):
            clientInfo = client
    if clientInfo == None:
        print(os.getenv("DOWNLOADCLIENT"),"not found")
    clientInfo["fields"][0]['value'] = transmissionIP

    # configure download client for sonarr
    sonarr = requests.put("http://" + os.getenv("SONARRHOST") + ":" + 
        os.getenv("SONARRPORT") +
        "/api/downloadclient/" + str(clientInfo["id"]) +
        "?apikey=" + os.getenv("SONARRAPIKEY"), data=json.dumps(clientInfo))
    print('sonarr PUT request status:', sonarr.status_code, '\n')


        # config radarr clients and connect to download clients
    radarr = requests.get("http://" + os.getenv("RADARRHOST") + ":" + 
        os.getenv("RADARRPORT") +
        "/api/downloadclient?apikey="+
        os.getenv("RADARRAPIKEY"))
    print('radarr GET request status:', radarr.status_code)
    
    # grab client info and configure
    clientInfo = None
    for client in radarr.json():
        if (str(client['name']) == str(os.getenv("DOWNLOADCLIENT"))):
            clientInfo = client
    if clientInfo == None:
        print(os.getenv("DOWNLOADCLIENT"),"not found")
    clientInfo["fields"][0]['value'] = transmissionIP

    # configure download client for sonarr
    radarr = requests.put("http://" + os.getenv("RADARRHOST") + ":" + 
        os.getenv("RADARRPORT") +
        "/api/downloadclient/" + str(clientInfo["id"]) +
        "?apikey=" + os.getenv("RADARRAPIKEY"), data=json.dumps(clientInfo))
    print('radarr PUT request status:', radarr.status_code, '\n')

except docker.errors.APIError:
    print('failed to connect to docker')
    # print(docker.errors.APIError)


