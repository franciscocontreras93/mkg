import os
import glob
import pandas as pd
os.chdir(r"F:\FRANCISCO\GIS\ISMAEL\BASES 2021\GEOCODING")
extension = 'xlsx'
total = 0

all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
for e in all_filenames:
    total += 1

combined_csv = pd.concat([pd.read_excel(f, engine="openpyxl") for f in all_filenames])
#export to csv
print(f"Se combinaron un total de {total} elementos")
combined_csv.to_csv("BASES-TDA-2021.csv", index=False, encoding='utf-8')


""" os.chdir(r"F:\FRANCISCO\GIS\ISMAEL\BASES 2020\respaldo\entrega")
for vLayer in iface.mapCanvas().layers():
    vLayerName = vLayer.name()

    QgsVectorFileWriter.writeAsVectorFormat(vLayer, f"{vLayerName[0:4]}.csv", "utf-8",
                                            vLayer.crs(), "CSV") """
