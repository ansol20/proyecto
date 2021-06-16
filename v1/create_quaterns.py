import json
import geojson 
#import shapely
#from shapely.geometry.point import Point


f = open('hospitales.json')
hospitales = json.load(f)
nombres = hospitales.keys()
Coordx1y1 = [-78.403930,-0.070038] #point Begin(x1,y1) x1=Longitud, y1=Latitud
Coordx2y1 = [-78.589325,-0.070038] #point Begin(x1,y2)
hopx= round( (Coordx2y1[0]-Coordx1y1[0])/50 , 6)    #Hop on x
Coordx1y2 = [-78.403930,-0.369069]
Coordx2y2 = [-78.589325,-0.369069]
hopy= round((Coordx1y2[1]-Coordx1y1[1])/50,6)

PositionXBegin = Coordx1y1[0]
PositionYBegin = Coordx1y1[1]


PositionXEnd = Coordx2y1[0]
PositionYEnd = Coordx1y2[1]
nodos=[]
i=1
j=0
n=0
m=0
cuadrantesData = { "type":"FeatureCollection","features":[]}
cantidadHospitalesCuadrante = {"cuadrantes":[],"cantidad":[]}
# Cluster, hospitales

cluster = []
while PositionXBegin >=  PositionXEnd-hopx:
    PositionYBegin = Coordx1y1[1]
    m=0
    while PositionYBegin >= PositionYEnd-hopy:
        gjson = {"type":"Feature","id":"c%d" %i,"properties":{"name":"cuadrante %d" %i},"geometry":{"type":"Polygon","coordinates":[[
            [ round(PositionXBegin,6), round(PositionYBegin,6)],
            [ round(PositionXBegin+hopx,6), round(PositionYBegin,6)],
            [ round(PositionXBegin+hopx,6), round(PositionYBegin+hopy,6)],
             [ round(PositionXBegin,6), round(PositionYBegin+hopy,6)]]]} }
        cuadrante = {}
        cuadrante["nombre"]= "cuadrante %d" %i
        cuadrante["posicion"] = [
            [ round(PositionXBegin,6), round(PositionYBegin,6)],
            [ round(PositionXBegin+hopx,6), round(PositionYBegin,6)],
            [ round(PositionXBegin+hopx,6), round(PositionYBegin+hopy,6)],
             [ round(PositionXBegin,6), round(PositionYBegin+hopy,6)]
            ]
        cuadrante["hospitales"] = []
        cuadrantesData["features"].append(gjson)
        c = {"cluster":[round(PositionYBegin+hopy/2,6),round(PositionXBegin+hopx/2,6)],"hospitales":[],"coordenada_red":[n,m]}
        for hospital in nombres:
            #print("Verificar cuadrante x:",round(PositionXBegin,6),round(PositionXBegin+hopx,6),round(hospitales[hospital][1],6),"\n","Verificar cuadrante y:", round(PositionYBegin,6),round(PositionYBegin+hopy,6),round(hospitales[hospital][0],6))
            if round(PositionXBegin,6) > round(hospitales[hospital][1],6) and round(PositionXBegin+hopx,6) < round(hospitales[hospital][1],6) and round(PositionYBegin,6) > round(hospitales[hospital][0],6) and round(PositionYBegin+hopy,6) < round(hospitales[hospital][0],6):
                cuadrante["hospitales"].append({"nombre":hospital,"localizacion":[round(hospitales[hospital][0],6),round(hospitales[hospital][1],6)]})
                c["hospitales"].append({"nombre":hospital,"localizacion":[round(hospitales[hospital][0],6),round(hospitales[hospital][1],6)]})
        """
        for hospital in cuadrante["hospitales"]:
            center = Point(hospital["localizacion"][1],hospital["localizacion"][0])          # Null Island
            circle = center.buffer(0.0001)  # Degrees Radius            
            gjsonHospital = {"type":"Feature","id":"h%d" %j, 
                            "properties":{"name":hospital["nombre"],"radius":len(cuadrante["hospitales"])},
                            "geometry":shapely.geometry.mapping(circle)}
            #                {"type":"Point","coordinates": [hospital["localizacion"][1],hospital["localizacion"][0]]}
            cuadrantesData["features"].append(gjsonHospital)
            cantidadHospitalesCuadrante["cuadrantes"].append("h%d" %j)
            cantidadHospitalesCuadrante["cantidad"].append(len(cuadrante["hospitales"]))
            j+=1
        """
        cantidadHospitalesCuadrante["cuadrantes"].append("c%d" %i)
        cantidadHospitalesCuadrante["cantidad"].append(len(cuadrante["hospitales"]))
        nodos.append(cuadrante)
        i+=1
        PositionYBegin+=hopy
        m+=1
        cluster.append(c)
        
    PositionXBegin+=hopx
    n+=1
print(m,n)
dataFinal = {"GJsonCuadrantes":cuadrantesData,"cantidad":cantidadHospitalesCuadrante,"clusters":cluster}
with open('cuadrantes.json', 'w') as outfile:
    json.dump(nodos, outfile)
with open('gjsoncuadrantes.json', 'w') as outfile:
    json.dump(dataFinal, outfile)
