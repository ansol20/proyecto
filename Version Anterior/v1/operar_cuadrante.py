import json
import math
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


f = open('gjsoncuadrantes.json')

cuadrantes = json.load(f)
clusters = cuadrantes["clusters"]
enlaces = []
for posicion in range(0,len(clusters)):
  enlace = {"coordenada_red":clusters[posicion]["coordenada_red"],"coordenadas":clusters[posicion]["cluster"],"hospitales":[], "cluster_alrededores":[]}
  for n in range(0,len(clusters[posicion]["hospitales"])):
    enlace["hospitales"].append({"nombre":clusters[posicion]["hospitales"][n]["nombre"],"coordenadas":clusters[posicion]["hospitales"][n]["localizacion"],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[posicion]["hospitales"][n]["localizacion"])})
  if clusters[posicion]["coordenada_red"][0]+1<=48:
    if clusters[posicion]["coordenada_red"][1]-1>=0:
      posicion_vector = (clusters[posicion]["coordenada_red"][0]+1)*49+clusters[posicion]["coordenada_red"][1]-1
      enlace_alrededor = {"coordenada_red":[clusters[posicion]["coordenada_red"][0]+1,clusters[posicion]["coordenada_red"][1]-1],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[posicion_vector]["cluster"]),"coordenadas":clusters[posicion_vector]["cluster"],"hospitales":[]}
      for n in range(0,len(clusters[posicion_vector]["hospitales"])):
        enlace_alrededor["hospitales"].append({"nombre":clusters[posicion_vector]["hospitales"][n]["nombre"],"coordenadas":clusters[posicion_vector]["hospitales"][n]["localizacion"],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion_vector]["cluster"],clusters[posicion_vector]["hospitales"][n]["localizacion"])})
      #agregar hospitales por punto y la distancia al cluster
      #posicion 0, es la x, posicion 1, es la y, posicion 3 es la distancia en km.
      #Encontramos el cuadrante el hospital, a partir del cuadrante, buscamos todos los clusters y hospitales en los cluster al rededor. 
      enlace["cluster_alrededores"].append(enlace_alrededor)
    enlace["cluster_alrededores"].append({"coordenada_red":[clusters[posicion]["coordenada_red"][0]+1,clusters[posicion]["coordenada_red"][1]],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[(clusters[posicion]["coordenada_red"][0]+1)*49+clusters[posicion]["coordenada_red"][1]]["cluster"]),"coordenadas":clusters[(clusters[posicion]["coordenada_red"][0]+1)*49+clusters[posicion]["coordenada_red"][1]]["cluster"]})
    if clusters[posicion]["coordenada_red"][1]+1<=48:
      enlace["cluster_alrededores"].append({"coordenada_red":[clusters[posicion]["coordenada_red"][0]+1,clusters[posicion]["coordenada_red"][1]+1],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[(clusters[posicion]["coordenada_red"][0]+1)*49+clusters[posicion]["coordenada_red"][1]+1]["cluster"]),"coordenadas":clusters[(clusters[posicion]["coordenada_red"][0]+1)*49+clusters[posicion]["coordenada_red"][1]+1]["cluster"]})
  if clusters[posicion]["coordenada_red"][1]-1>=0:
    enlace["cluster_alrededores"].append({"coordenada_red":[clusters[posicion]["coordenada_red"][0],clusters[posicion]["coordenada_red"][1]-1],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[(clusters[posicion]["coordenada_red"][0])*49+clusters[posicion]["coordenada_red"][1]-1]["cluster"]),"coordenadas":clusters[(clusters[posicion]["coordenada_red"][0])*49+clusters[posicion]["coordenada_red"][1]-1]["cluster"]})

  if clusters[posicion]["coordenada_red"][1]+1<=48:
    posicion_vector = (clusters[posicion]["coordenada_red"][1]+1)*49+clusters[posicion]["coordenada_red"][1]+1
    enlace_alrededor = {"coordenada_red":[clusters[posicion]["coordenada_red"][1]+1,clusters[posicion]["coordenada_red"][1]+1],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[posicion_vector]["cluster"]),"coordenadas":clusters[posicion_vector]["cluster"],"hospitales":[]}
    for n in range(0,len(clusters[posicion_vector]["hospitales"])):
        enlace_alrededor["hospitales"].append({"nombre":clusters[posicion_vector]["hospitales"][n]["nombre"],"coordenadas":clusters[posicion_vector]["hospitales"][n]["localizacion"],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion_vector]["cluster"],clusters[posicion_vector]["hospitales"][n]["localizacion"])})
    #enlace["cluster_alrededores"].append({"coordenada_red":[clusters[posicion]["coordenada_red"][0],clusters[posicion]["coordenada_red"][1]+1],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[(clusters[posicion]["coordenada_red"][0])*49+clusters[posicion]["coordenada_red"][1]+1]["cluster"]),"coordenadas":clusters[(clusters[posicion]["coordenada_red"][0])*49+clusters[posicion]["coordenada_red"][1]+1]["cluster"]})
  if clusters[posicion]["coordenada_red"][0]-1>=0:
    if clusters[posicion]["coordenada_red"][1]-1>=0:
      enlace["cluster_alrededores"].append({"coordenada_red":[clusters[posicion]["coordenada_red"][0]-1,clusters[posicion]["coordenada_red"][1]-1],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[(clusters[posicion]["coordenada_red"][0]-1)*49+clusters[posicion]["coordenada_red"][1]-1]["cluster"]),"coordenadas":clusters[(clusters[posicion]["coordenada_red"][0]-1)*49+clusters[posicion]["coordenada_red"][1]-1]["cluster"]})
    enlace["cluster_alrededores"].append({"coordenada_red":[clusters[posicion]["coordenada_red"][0]-1,clusters[posicion]["coordenada_red"][1]],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[(clusters[posicion]["coordenada_red"][0]-1)*49+clusters[posicion]["coordenada_red"][1]]["cluster"]),"coordenadas":clusters[(clusters[posicion]["coordenada_red"][0]-1)*49+clusters[posicion]["coordenada_red"][1]]["cluster"]})
    if clusters[posicion]["coordenada_red"][1]+1<=48:
      posicion_vector = (clusters[posicion]["coordenada_red"][1]+1)*49+clusters[posicion]["coordenada_red"][1]+1
    enlace_alrededor = {"coordenada_red":[clusters[posicion]["coordenada_red"][1]+1,clusters[posicion]["coordenada_red"][1]+1],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[posicion_vector]["cluster"]),"coordenadas":clusters[posicion_vector]["cluster"],"hospitales":[]}
    for n in range(0,len(clusters[posicion_vector]["hospitales"])):
        enlace_alrededor["hospitales"].append({"nombre":clusters[posicion_vector]["hospitales"][n]["nombre"],"coordenadas":clusters[posicion_vector]["hospitales"][n]["localizacion"],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion_vector]["cluster"],clusters[posicion_vector]["hospitales"][n]["localizacion"])})
      #enlace["cluster_alrededores"].append({"coordenada_red":[clusters[posicion]["coordenada_red"][0]-1,clusters[posicion]["coordenada_red"][1]+1],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["cluster"],clusters[(clusters[posicion]["coordenada_red"][0]-1)*49+clusters[posicion]["coordenada_red"][1]+1]["cluster"]),"coordenadas":clusters[(clusters[posicion]["coordenada_red"][0]-1)*49+clusters[posicion]["coordenada_red"][1]+1]["cluster"]})   
  enlaces.append(enlace)
print(enlaces)
with open('/Users/Ansol/Desktop/enlaces.json', 'w') as outfile:
    json.dump(enlaces, outfile)
#
# 
# print(distanceInKmBetweenEarthCoordinates(clusters[0]["cluster"],clusters[1]["cluster"]))

#for i in cuadrantes:
#    print(len(i["hospitales"]))