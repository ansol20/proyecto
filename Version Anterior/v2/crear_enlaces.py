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

def definir_enlace(posicion,enlace_posicion,clusters):
  return {"coordenada":clusters[enlace_posicion-1]["coordenada"],"nombre":"cluster_%d" %enlace_posicion, 
                      "distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion]["coordenada"],clusters[enlace_posicion-1]["coordenada"])}

clusters = json.load(open('clusters.json'))

enlaces = []
for posicion in range(0,len(clusters)):
  print(clusters[posicion])
  #Principal con los hospitales
  numero_de_cluster = clusters[posicion]["coordenada_red"][0]*10+ clusters[posicion]["coordenada_red"][1]+1
  enlace = {"origen":"cluster_%d" %numero_de_cluster,"coordenada":clusters[posicion]["coordenada"],"destinos":[]}
  for hospital in clusters[posicion]["hospitales"]:
    hospital["distancia"] = distanceInKmBetweenEarthCoordinates(clusters[posicion]["coordenada"],hospital["coordenadas"])
    enlace["destinos"].append(hospital)
  #3 posibilidades:
  #1. H1-C1 / C1-C2 / C2-H2
  #2. H1-C2 / C2-H2
  #3. H1-H2
  #for hospital in clusters[numero_de_cluster_enlace-1]["hospitales"]:
  #  enlace_alrededor["hospitales"].append({"nombre":clusters[posicion_vector]["hospitales"][n]["nombre"],"coordenadas":clusters[posicion_vector]["hospitales"][n]["localizacion"],"distancia":distanceInKmBetweenEarthCoordinates(clusters[posicion_vector]["cluster"],clusters[posicion_vector]["hospitales"][n]["localizacion"])})
  #agregar hospitales por punto y la distancia al cluster
  #posicion 0, es la x, posicion 1, es la y, posicion 3 es la distancia en km.
  #Encontramos el cuadrante el hospital, a partir del cuadrante, buscamos todos los clusters y hospitales en los cluster al rededor. 
  
  #Enlace con latitud anterior y longitud anterior
  if clusters[posicion]["coordenada_red"][0]-1>=0 and clusters[posicion]["coordenada_red"][1]-1>=0:
      enlace["destinos"].append(definir_enlace(posicion,(clusters[posicion]["coordenada_red"][0]-1)*10+ clusters[posicion]["coordenada_red"][1],clusters))
  #Enlace sin alterar latitud con longitud anterior 
  if clusters[posicion]["coordenada_red"][1]-1>=0:
      enlace["destinos"].append(definir_enlace(posicion,clusters[posicion]["coordenada_red"][0]*10+ clusters[posicion]["coordenada_red"][1],clusters))
  #Enlace con latitud posterior y longitud anterior
  if clusters[posicion]["coordenada_red"][0]+1<=9 and clusters[posicion]["coordenada_red"][1]-1>=0: 
      enlace["destinos"].append(definir_enlace(posicion,(clusters[posicion]["coordenada_red"][0]+1)*10+ clusters[posicion]["coordenada_red"][1],clusters))

  #Enlace con latitud anterior sin alterar longitud .
  if clusters[posicion]["coordenada_red"][0]-1>=9:
    enlace["destinos"].append(definir_enlace(posicion,(clusters[posicion]["coordenada_red"][0]-1)*10+ clusters[posicion]["coordenada_red"][1]+1,clusters))

  #Enlace con latitud posterior sin alterar longitud .
  if clusters[posicion]["coordenada_red"][0]+1<=9:
    enlace["destinos"].append(definir_enlace(posicion,(clusters[posicion]["coordenada_red"][0]+1)*10+ clusters[posicion]["coordenada_red"][1]+1,clusters))

  #Enlace con latitud anterior y longitud posterior
  if clusters[posicion]["coordenada_red"][0]-1>=0 and clusters[posicion]["coordenada_red"][1]+1<=9:
      enlace["destinos"].append(definir_enlace(posicion,(clusters[posicion]["coordenada_red"][0]-1)*10+ clusters[posicion]["coordenada_red"][1]+2,clusters))
  #Enlace sin alterar latitud con longitud posterior
  if clusters[posicion]["coordenada_red"][1]+1<=9:
     enlace["destinos"].append(definir_enlace(posicion,clusters[posicion]["coordenada_red"][0]*10+ clusters[posicion]["coordenada_red"][1]+2,clusters))
  #Enlace con latitud posterior y longitud posterior
  if clusters[posicion]["coordenada_red"][0]+1<=9 and clusters[posicion]["coordenada_red"][1]+1<=9:
      enlace["destinos"].append(definir_enlace(posicion,(clusters[posicion]["coordenada_red"][0]+1)*10+ clusters[posicion]["coordenada_red"][1]+2,clusters))



  enlaces.append(enlace)
with open('enlaces.json', 'w') as outfile:
    json.dump(enlaces, outfile)

#
# 
# print(distanceInKmBetweenEarthCoordinates(clusters[0]["cluster"],clusters[1]["cluster"]))

#for i in cuadrantes:
#    print(len(i["hospitales"]))