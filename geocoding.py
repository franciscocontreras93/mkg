import geocoder
import folium.map
import sys
import os
import glob
import pandas as pd
import unidecode
from geopy.geocoders import Here, Nominatim, OpenMapQuest, GoogleV3
from tqdm import tqdm
import time

os.chdir(r"C:\Users\FRANCISCO\Desktop\geocoding")
all_filenames = [i for i in glob.glob('*.{}'.format('xlsx'))]
mapquest_api_key = "ICyLfqteowXxftrsVWt4SpGIeycWVUXJ" # APIKEY MAPQUEST
here_app_id = "gDYP3rI1xGkpcY4Xmr13" # APP ID HERE TECHNOLOGY
here_api_key = "sY9mFdYg4L-vkiS6n8BZmAV8Y_2fENdhd8fPT9WWngk"  # API KEY HERE TECHNOLOGY 
google_api_key = "AIzaSyDeAxeJFDKW0vkYODqmnVevH3ZLYWgvU2w"  # API KEY GOOGLE
# GEOCODERS #
nominatim = Nominatim(user_agent="franciscocontreras93@gmail.com")
here = Here(apikey=here_api_key)
mapquest = OpenMapQuest(api_key=mapquest_api_key)
googlev3 = GoogleV3(google_api_key)

geocoders = [here, nominatim, mapquest, googlev3]  # ,here,mapquest, googlev3
#--------------#

# codec = "ISO-8859-1"
# codec2 ="utf8"

print(""" ESTE PROGRAMA ESTA DESARROLADO PARA USO EXCLUSIVO DE GEOSIG /n""")

file_name = input("ingrese el nombre del archivo:   ")
file = f"{file_name}.xlsx"
data = pd.read_excel(file, engine="openpyxl")
df = pd.DataFrame(data)
ciudad = df["Q274"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
colonia = df["col"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
direccion = "Colonia " + colonia + " , " + ciudad + " , Mexico"

latitud = []
longitud = []
codec = []





def coding(address):
    i = 0
    try:
        while i < len(geocoders):
            location = geocoders[i].geocode(address)
            
            if location != None:
                lat = location.latitude 
                long = location.longitude
                latitud.append(lat)
                longitud.append(long)
                codec.append(i)
                # print(f"exitoso")
                break
            else:
                i += 1
    except:
        lat = 0
        long = 0
        codec.append("error")
        latitud.append(lat)
        longitud.append(long)
        # print(f"X = {long} Y = {lat}")
        #print(f"No se encontro la direccion")
    return latitud,longitud


def codificar(campo): 

    print("geocodificando...",file, len(campo))
    e = 0

    for elemento in campo:
        e += 1
        coding(elemento)
        # print(elemento)
        print(f"{int(e * 100 / len(campo))} %")
    print(f"finalizado...")








inicio = time.time()
codificar(direccion)
fin = time.time()
df['LATITUD'] = latitud
df['LONGITUD'] = longitud
df['CODEC'] = codec
df.to_csv(f"{file[:-5]}-PROCESS.csv")
print(f"tiempo de ejecucion: {fin-inicio}")


