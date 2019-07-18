#!/usr/bin/python3
# Project 1 to IPK, variant 2
# Author: Adam Janda, xjanda26@stud.fit.vutbr.cz, VUT FIT 2019

import socket
import json
import sys

key = sys.argv[1]
city = sys.argv[2]

server = 'api.openweathermap.org'
port = 80

getLink = '/data/2.5/weather?q={}&appid={}&units=metric'.format(city, key)

reque = "GET "+getLink+"\r\nHTTP/1.0\r\nHost "+server+"\r\nConnection: close\r\n\r\n"
requeB = str.encode(reque)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    try:
        soc.connect((server, port))
        soc.sendall(requeB)
        data = soc.recv(2048)
    except socket.timeout:
        sys.stderr.write("Error! Connection lost.\n")
        sys.exit(1)

decodeData = json.loads(data)

if (decodeData['cod'] == 401 ):
    sys.stderr.write("Error! {}.\n".format(decodeData['message']))
    sys.exit(401)   

if 'name' in decodeData:
    print("City: {}".format(decodeData['name']))
else:
    sys.stderr.write("Error! {}.\n".format(decodeData['message']))
    sys.exit(404)


print (decodeData['weather'][0]['description'])
print ("Temperature: {} degrees Celsius".format(decodeData['main']['temp']))
if 'humidity' in decodeData['main']:
    print ("Humidity: {}%".format(decodeData['main']['humidity']))

if 'pressure' in decodeData['main']:
    print ("Preassure: {}hPa".format(decodeData['main']['pressure']))
else:
    print ("Preassure:-")

if 'wind' in decodeData:
    if 'speed' in decodeData['wind']:
        print ("Wind speed: {}km/s".format(decodeData['wind']['speed']))
    else:
        print ("Wind speed: 0km/h")

    if 'deg' in decodeData['wind']:
        print ("Wind degrees: {}".format(decodeData['wind']['deg']))
    else:
        print ("Wind degrees:-")

else:
    print ("Wind speed: 0km/h\nWind degrees:-")
