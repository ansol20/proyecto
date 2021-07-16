import http.server
import socketserver
import networkx as nx
import pandas as pd
import json
import base64
import math

df = pd.read_json('hospitales_data_final.json')
cdf = pd.read_json('centroides_final.json')

hospitales_data = {}
for k in range(3,11):
    hospitales_data["cdf_%d" %k] = pd.read_json('centroides_final_%d.json' %k)


def calcular_distancia_euclidean(cord1,cord2):
    return math.sqrt((cord1[0]-cord2[0])**2 +(cord1[1]-cord2[1])**2+(cord1[2]-cord2[2])**2) #Calcular la distancia entre dos puntos con coordenadas cartesianas x,y,z


PORT = 8010

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            fh=open('index.html','rb')
            string=fh.read()
            self.wfile.write(string)
        elif self.path.find('hospitales_data_final')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fh=open('hospitales_data_final.json','rb')
            string=fh.read()
            self.wfile.write(string)                                                                                              
        elif self.path.find('hospital42.png')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            fh=open('hospital42.png','rb')
            string=fh.read()
            self.wfile.write(string)     
        elif self.path.find('centroides_final')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fh=open('centroides_final.json','rb')
            string=fh.read()
            self.wfile.write(string)    
        elif self.path.find('centroides_final_3')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fh=open('centroides_final_3.json','rb')
            string=fh.read()
            self.wfile.write(string)    
        elif self.path.find('centroides_final_4')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fh=open('centroides_final_4.json','rb')
            string=fh.read()
            self.wfile.write(string)    
        elif self.path.find('centroides_final_5')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fh=open('centroides_final_5.json','rb')
            string=fh.read()
            self.wfile.write(string)                                                   
        elif self.path.find('centroides_final_6')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fh=open('centroides_final_6.json','rb')
            string=fh.read()
            self.wfile.write(string)    
        elif self.path.find('centroides_final_7')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fh=open('centroides_final_7.json','rb')
            string=fh.read()
            self.wfile.write(string)    
        elif self.path.find('centroides_final_8')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fh=open('centroides_final_8.json','rb')
            string=fh.read()
            self.wfile.write(string)    
        elif self.path.find('centroides_final_9')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fh=open('centroides_final_9.json','rb')
            string=fh.read()
            self.wfile.write(string) 
        elif self.path.find('centroides_final_10')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            fh=open('centroides_final_10.json','rb')
            string=fh.read()
            self.wfile.write(string)                                                                               
        elif self.path.find('request_min_path')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            values = {}
            
            if '?' in self.path:
                data = self.path.split('?', 1)[1].split('&')
                for n in data:
                    d = n.split("=")
                    values[d[0]] = float(d[1])    
                    if d[0]=="ncluster" :
                        values[d[0]] = int(d[1])    
              
            data = {}
            maxima_distancia = values["distancia_maxima"]
            if len(values.keys())>0 :
                if values["data"]==0:
                    G=nx.Graph()
                    for index, row in df.iterrows():
                        G.add_node(row["id"],pos=(row["cartesianas"][0],row["cartesianas"][1]))
                        if row["distancia_centro_%s" %values["ncluster"]] !=0 :
                            G.add_edge(row["hospitales_centros_%s" %values["ncluster"]],row["id"],weight=row["distancia_centro_%s" %values["ncluster"]])

                    for index, row in hospitales_data["cdf_%s" %values["ncluster"]].iterrows():
                        if row["distancias_%s" %values["ncluster"]] < maxima_distancia:
                            G.add_edge(row["inicio_%s" %values["ncluster"]],row["final_%s" %values["ncluster"]],weight=row["distancias_%s" %values["ncluster"]])

                    rute=[]
                    try:
                        rute=nx.shortest_path(G, values["inicio"],values["final"],weight="weight")
                    except nx.NetworkXNoPath:
                        print("No path")
                    data = {"ruta":rute}

                else:
                    G2=nx.Graph()
                    print("iniciando ...")
                    for index, row in df.iterrows():
                        G2.add_node(row["id"],pos=(row["cartesianas"][0],row["cartesianas"][1]))
                    cantidad_de_nodos=len(df["cartesianas"])
                    print(calcular_distancia_euclidean(df["cartesianas"][values["inicio"]],df["cartesianas"][values["final"]]))
                    for i in range(0,cantidad_de_nodos):
                        for j in range(0,cantidad_de_nodos):
                            if calcular_distancia_euclidean(df["cartesianas"][i],df["cartesianas"][j])<maxima_distancia and i!=j:
                                G2.add_edge(i,j,weight=calcular_distancia_euclidean(df["cartesianas"][i],df["cartesianas"][j]))
                    print("terminando ...")
                    rute=[]
                    try:
                        rute=nx.shortest_path(G2, values["inicio"],values["final"],weight="weight")
                    except nx.NetworkXNoPath:
                        print("No path")
                    data = {"ruta":rute}
            json_object = json.dumps(data)  
            self.wfile.write(bytes(json_object, "utf8"))
        return 

Handler = MyRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
