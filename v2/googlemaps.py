import requests
import json
import copy
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'


def verificar_no_hospital(hospitales,nombre_hospital):
    for i in hospitales:
        if i["nombre"]==nombre_hospital:
            return False
    return True

#Longitud = x [1]
#Latitud = y [0]
esquina_cuadrado_derecha_superior = [-0.070038,-78.403930]
esquina_cuadrado_izquierda_superior = [-0.070038,-78.589325]
salto_logintud = (esquina_cuadrado_derecha_superior[1]-esquina_cuadrado_izquierda_superior[1])/10

esquina_cuadrado_derecha_inferior = [-0.369069,-78.403930]
esquina_cuadrado_izquierda_inferior = [-0.369069,-78.589325]
salto_latitud = (esquina_cuadrado_derecha_inferior[0]-esquina_cuadrado_derecha_superior[0])/10

posicion_longitud_inicial = esquina_cuadrado_izquierda_superior[1]
posicion_latitud_inicial = esquina_cuadrado_izquierda_superior[0]

posicion_longitud_final = esquina_cuadrado_derecha_superior[1]
posicion_latitud_final = esquina_cuadrado_izquierda_inferior[0]


hospitales = []
posicion_salto_latitud = posicion_latitud_inicial

while posicion_salto_latitud >  posicion_latitud_final:
    print(posicion_latitud_final,posicion_salto_latitud)
    posicion_salto_longitud = posicion_longitud_inicial
    while posicion_salto_longitud < posicion_longitud_final:
        print(posicion_longitud_final,posicion_salto_longitud)
        radius = "3000"
        params = {
                    'location': "%.6f,%.6f" %(posicion_salto_latitud,posicion_salto_longitud),
                    'radius': radius,
                    'name': "hospital",
                    'key': "AIzaSyCt8zprmqILOnD_62f-fy9BTW36FceITqw"
        }
       
        # Do the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()
        for hospital in res["results"]:
            if verificar_no_hospital(hospitales,hospital["name"]):
                hospitales.append({"coordenadas":[round(hospital["geometry"]["location"]["lat"],6),round(hospital["geometry"]["location"]["lng"],6)],"nombre":hospital["name"]})
        params = {
                    'location': "%.6f,%.6f" %(posicion_salto_latitud,posicion_salto_longitud),
                    'radius': radius,
                    'name': "IESS",
                    'key': "AIzaSyCt8zprmqILOnD_62f-fy9BTW36FceITqw"
        }
       
        # Do the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()
        for hospital in res["results"]:
            if verificar_no_hospital(hospitales,hospital["name"]):
                hospitales.append({"coordenadas":[round(hospital["geometry"]["location"]["lat"],6),round(hospital["geometry"]["location"]["lng"],6)],"nombre":hospital["name"]})        
        
        posicion_salto_longitud=round(posicion_salto_longitud+salto_logintud, 6)

    posicion_salto_latitud=round(posicion_salto_latitud+salto_latitud, 6)

with open('hospitales.json', 'w') as outfile:
    json.dump(hospitales, outfile)

