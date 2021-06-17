import json

f = open('hospitales.json')
total_hospitales = json.load(f)

def excluir_hospitales(hospital,arreglo_exclusiones):
    for i in arreglo_exclusiones:
        if hospital==i:
            return True
    return False

exclusiones = ["Hospital","Centro Médico Familias Saludables","Hospital Calderon","CRUZ ROJA","Hospital Del Dia","Servidores Del Iess",
"Terreno en venta Coop Servidores del IESS","Iess Unidad Medica Sur Occidental","IESS",
"IEES-Punto de Atención, Quito Norte","DIRECCION NACIONAL DE GESTION ARCHIVO NORTE IESS",
"Centro Atención Iess","Frente Al Parque De Los Recuerdos","Centro de Salud E1","Laboratorio Hospital Metropolitano",
"GMEDIQ Cirugía General y Laparoscópica Ambato","Computer Hospital","Centro Medico La Florida","Medipet",
"Ambulatorio IESS","Hospital del dia Niños de la mano de María","AXXIS Integral Medical Center",
"REUMATOLOGO Quito, AXXIS HOSPITAL-Dr. Patricio López- Torre 2, piso 7","Labor risks IESS",
"Cruz Roja Sede Cochapata","IESS-SEGURO SOCIAL CAMPESINO","Banco del IESS","Exequiales IESS",
"BIESS","IEES MONTE DE PIEDAD","MUNDINET, servicio de papeleria, SRI, IESS, AMT, MUNICIPIO DE QUITO, MINISTERIO LABORAL","Unidad Oncologica SOLCA",
"Iess", "Talleres Iess Quito Pichincha","HEE","Ecuadorian Institute of Social Security - IESS", 
"Iees Quito","Bldg. Zarzuela IESS","IESS Direccion Provincial","Building Parque de Mayo IESS",
"Talleres Jubilados IESS", "Hospital Iess","Asesores y Facilitadores en trámites del IESS, Min del Trabajo - asesfacil",
"Centro de jubilados Iess Amazonas","BiciQ - Estación IESS","HCAM","Baca Ortiz Pediatric Hospital","IESS PARQUE DE MAYO",
"Centro Medico Familiar IESS","Colon","Hospital Veterinario de Especialidades USFQ","Plaza Hospital de Los Valles USFQ",
"Edificio Especialidades Médicas","Hospital Docente de Especialidades Veterinarias USFQ","IESS - Point of Care",
"Agencia IESS Tumbaco","Iess Santo Domingo","Dispendario IESS Beaterio","UNIDADES MÉDICAS I.E.S.S.",
"Subcentro de Salud N°04","IESS agency - Villaflora","Biess Pawnshop","Centro Medico IESS Chimbacalle",
"dispensario iess", "Veterinaria U central","Dr. Carlos Bracho Velasco",
"DR. PEDRO LOVATO","Iess South Hospital","HOSPITAL OF THE DAY ELOY ALFARO",
"Hospital IESS Andrea","COOPERATIVA DE VIVIENDA IESS-FUT","Disoloxi Medicinal Hospital IESS Quito Sur",
"Omnilife Seytu El Calzado Hospital IESS","Exequiales Iess","Centro de atención IESS","Dispensario Del Sur Del Iess","Iess Punto De Atención",
"Hospital Veterinario Lucky","Hospital Veterinario MedicVet","IESS La Ecuatoriana","hospital solca","Centro Medico Iess",
"hospital iess sangolqui","IESS Agencia River Mall","Hospital emergencias San Francisco","Hosteria Los Cactus IESS",
"Centro De Salud Uyumbicho","Centro Medico IESS Amaguaña","Subcentro de salud de cotogchoa"]

hmaxlat =""
max_latitude=-1000
hminlat =""
min_latitude=1000

hmaxlong = ""
max_longitude=-1000
hminlong = ""
min_longitude=1000
hospitales = []

#excluyo los hospitales con (exclusiones-depuracion manual)
for hospital in total_hospitales:
    if not excluir_hospitales(hospital["nombre"],exclusiones):
        hospitales.append(hospital)
numero = 1 
for hospital in hospitales:
    #print(numero,". ", hospital["nombre"],hospital["coordenadas"])
    numero+=1
    if max_latitude < hospital["coordenadas"][0]:
        max_latitude = hospital["coordenadas"][0]
        hmaxlat = hospital["nombre"]
    if min_latitude >  hospital["coordenadas"][0]:
        min_latitude =  hospital["coordenadas"][0]
        hminlat = hospital["nombre"]
    if max_longitude < hospital["coordenadas"][1]:
        max_longitude = hospital["coordenadas"][1]
        hmaxlong = hospital["nombre"]
    if min_longitude > hospital["coordenadas"][1]:
        min_longitude = hospital["coordenadas"][1]
        hminlong = hospital["nombre"]
with open('SoloHospitales.json', 'w') as outfile:
    json.dump(hospitales, outfile)
CoordenadasMaximas = {"superior_izquierda":[max_latitude,min_longitude],"superior_derecha":[max_latitude, max_longitude],
                      "inferior_izquierda":[min_latitude,min_longitude],"inferior_derecha":[min_latitude,max_longitude]}


#comprobar CoordenadasMaximas
with open('CoordenadasMaximas.json', 'w') as outfile:
    json.dump(CoordenadasMaximas, outfile)

