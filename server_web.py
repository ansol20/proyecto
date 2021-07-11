import http.server
import socketserver
import networkx as nx
import pandas as pd
import json
import base64

df = pd.read_json('hospitales_data_final.json')
cdf = pd.read_json('centroides_final.json')
maxima_distancia = 13

G=nx.Graph()
for index, row in df.iterrows():
    G.add_node(row["id"],pos=(row["cartesianas"][0],row["cartesianas"][1]))
    if row["distancia_centro"] !=0 :
        G.add_edge(row["hospitales_centros"],row["id"],weight=row["distancia_centro"])

for index, row in cdf.iterrows():
    if row["distancias"] < maxima_distancia:
        G.add_edge(row["inicio"],row["final"],weight=row["distancias"])

pos=nx.get_node_attributes(G,'pos')
nx.draw(G,pos)

PORT = 8000

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
        elif self.path.find('request_min_path')>0:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            values = {}
            
            if '?' in self.path:
                data = self.path.split('?', 1)[1].split('&')
                for n in data:
                    d = n.split("=")
                    values[d[0]] = int(d[1])    
              
            data = {}
            if len(values.keys())>0 :
                data = {"ruta":nx.shortest_path(G, values["inicio"],values["final"])}
            json_object = json.dumps(data)  
            self.wfile.write(bytes(json_object, "utf8"))
        return 

Handler = MyRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
