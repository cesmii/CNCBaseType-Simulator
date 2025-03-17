#!/usr/bin/env python
sim = {
    "sink": "smip",
    "samplerate": 10
}
smip = {
    "authenticator": "authenticator name",
    "password": "authenticator password",
    "name": "username",
    "role": "ROLE",
    "url": "https://sandbox.cesmii.net/graphql",
    "verbose": True
}
mqtt = {
    "broker": "192.168.10.5",
    "port": 8883,
    "clientid": "cncsim",
    "username": "YOURUSER",
    "password": "YOURPASSWORD",
    "tls": True,
    "protocol": 311,
    "topic": "mycnc"
}
