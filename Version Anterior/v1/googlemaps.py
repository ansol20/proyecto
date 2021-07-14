import requests
import json
import copy
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

beginp1 = [-0.070038,-78.403930]
beginp2 = [-0.070038,-78.589325]
hopx= (beginp2[1]-beginp1[1])/10
beginp3 = [-0.369069,-78.403930]
beginp4 = [-0.369069,-78.589325]

positionx = beginp2[0]
positiony = beginp1[1]

nodos=[]



while positionx >  beginp3[0]:
    positiony = beginp1[1]
    while positiony > beginp2[1]:
        radius = "5000"
        params = {
                    'location': "%.6f,%.6f" %(positionx,positiony),
                    'radius': radius,
                    'types': "hospital",
                    'key': "AIzaSyCt8zprmqILOnD_62f-fy9BTW36FceITqw"
        }
        positiony+=hopx
        positiony=round(positiony, 6)
        # Do the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()

        nodo={}
        nodo["Posicion"]={}
        nodo["Posicion"]["nodo"]=[positionx,positiony]
        nodo["Posicion"]["hospitales"]=[]
        for i in res['results']:
            hospital={}
            hospital["localizacion"] = [round(i["geometry"]["location"]["lat"],6),round(i["geometry"]["location"]["lng"],6)]
            hospital["nombre"] = i["name"]
            nodo["Posicion"]["hospitales"].append(hospital)
        nodos.append(nodo)
        print(nodo)
    positionx+=hopx   
    positionx=round(positionx, 6)
    
print(nodos)

hospitales = {}
for i in nodos:
    for n in i["Posicion"]["hospitales"]:
        hospitales[n["nombre"]] = n["localizacion"]
        
with open('hospitales.json', 'w') as outfile:
    json.dump(hospitales, outfile)

with open('data.json', 'w') as outfile:
    json.dump(nodos, outfile)