import os
import glob
import pandas as pd
os.chdir("C:\\ISMAEL\\entregas\\csv\\10bases2")
extension = 'csv'
total = 0

all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
for e in all_filenames:
    total += 1

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
#export to csv
print(f"Se combinaron un total de {total} elementos")
combined_csv.to_csv("35Bases.csv", index=False, encoding='system')


""" os.chdir(r"F:\FRANCISCO\GIS\ISMAEL\BASES 2020\respaldo\entrega")
for vLayer in iface.mapCanvas().layers():
    vLayerName = vLayer.name()

    QgsVectorFileWriter.writeAsVectorFormat(vLayer, f"{vLayerName[0:4]}.csv", "utf-8",
                                            vLayer.crs(), "CSV") """
