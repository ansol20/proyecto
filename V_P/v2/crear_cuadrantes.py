import json
import geojson 
import math

#import shapely
#from shapely.geometry.point import Point
def degreesToRadians(degrees):
  return degrees * math.pi / 180

def distanceInKmBetweenEarthCoordinates(pos1, pos2):
  earthRadiusKm = 6371
  dLon = degreesToRadians(pos2[1]-pos1[1])
  dLat = degreesToRadians(pos2[0]-pos1[0])

  lat1 = degreesToRadians(pos1[0])
  lat2 = degreesToRadians(pos2[0])

  a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2); 
  c = 2 * math.asin(math.sqrt(a)); 
  return earthRadiusKm * c


cuadrante = json.load(open('CoordenadasMaximas.json'))
hospitales = json.load(open('SoloHospitales.json'))
#Longitud = x [1]
#Latitud = y [0]
esquina_cuadrado_izquierda_superior = [round(cuadrante["superior_izquierda"][0]+0.00001,6),round(cuadrante["superior_izquierda"][1]-0.00001,6)]
esquina_cuadrado_derecha_superior = [round(cuadrante["superior_derecha"][0]+0.00001,6),round(cuadrante["superior_derecha"][1]+0.00001,6)]

esquina_cuadrado_derecha_inferior = [round(cuadrante["inferior_derecha"][0]-0.00001,6),round(cuadrante["inferior_derecha"][1]+0.00001,6)]
esquina_cuadrado_izquierda_inferior = [round(cuadrante["inferior_izquierda"][0]-0.00001,6),round(cuadrante["inferior_izquierda"][1]-0.00001,6)]


salto_logintud = (esquina_cuadrado_derecha_superior[1]-esquina_cuadrado_izquierda_superior[1])/10
salto_latitud = (esquina_cuadrado_derecha_inferior[0]-esquina_cuadrado_derecha_superior[0])/10

posicion_longitud_inicial = esquina_cuadrado_izquierda_superior[1]
posicion_latitud_inicial = esquina_cuadrado_izquierda_superior[0]

posicion_longitud_final = esquina_cuadrado_derecha_superior[1]
posicion_latitud_final = esquina_cuadrado_izquierda_inferior[0]

posicion_salto_latitud = posicion_latitud_inicial
cuadrantes_gjson = []
cuadrantes = []
clusters = []
i=1
n=0
print(posicion_salto_latitud +salto_latitud,posicion_latitud_final)
while posicion_salto_latitud >  posicion_latitud_final:
    #print(posicion_salto_latitud,posicion_latitud_final)
    posicion_salto_longitud = posicion_longitud_inicial
    m=0
    while posicion_salto_longitud < posicion_longitud_final:
        cuadrante = [
                     [ round(posicion_salto_latitud,6), round(posicion_salto_longitud,6)],
                     [ round(posicion_salto_latitud,6), round(posicion_salto_longitud+salto_logintud,6)],
                     [ round(posicion_salto_latitud+salto_latitud,6), round(posicion_salto_longitud+salto_logintud,6)],
                     [ round(posicion_salto_latitud+salto_latitud,6), round(posicion_salto_longitud,6)],
                     [ round(posicion_salto_latitud,6), round(posicion_salto_longitud,6)]
                    ]
        cuadrantes_gjson.append({"type":"Feature","id":"c%d" %i,"properties":{"name":"cuadrante %d" %i},
                          "geometry":{"type":"Polygon","coordinates":[cuadrante]}})
        cuadrante_con_hospital = {"nombre":"cuadrante %d" %i,"posicion":cuadrante,"hospitales":[]}
        cluster = {"coordenada_red":[n,m],"coordenada":[round(posicion_salto_latitud+salto_latitud/2,6),round(posicion_salto_longitud+salto_logintud/2,6)],"hospitales":[]}
         
        for hospital in hospitales:
            if round(posicion_salto_longitud,6) < round(hospital["coordenadas"][1],6) and round(posicion_salto_longitud+salto_logintud,6) > round(hospital["coordenadas"][1],6) and round(posicion_salto_latitud,6) > round(hospital["coordenadas"][0],6) and round(posicion_salto_latitud+salto_latitud,6) < round(hospital["coordenadas"][0],6):
                cuadrante_con_hospital["hospitales"].append(hospital)
                cluster["hospitales"].append(hospital)
        cuadrantes.append(cuadrante_con_hospital)
        clusters.append(cluster)
        posicion_salto_longitud=round(posicion_salto_longitud+salto_logintud, 6)
        i+=1
        m+=1
    n+=1
    posicion_salto_latitud=round(posicion_salto_latitud+salto_latitud, 6)       
#print("Horizontal",distanceInKmBetweenEarthCoordinates(esquina_cuadrado_izquierda_superior,esquina_cuadrado_derecha_superior))
# print("Vertical",distanceInKmBetweenEarthCoordinates(esquina_cuadrado_derecha_inferior,esquina_cuadrado_derecha_superior))

with open('cuadrantes_mapa_geojson.json', 'w') as outfile:
    json.dump(cuadrantes_gjson, outfile)

with open('cuadrantes_data.json', 'w') as outfile:
    json.dump(cuadrantes, outfile)

with open('clusters.json', 'w') as outfile:
    json.dump(clusters, outfile)