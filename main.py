from jinja2 import Environment, PackageLoader
from jinja2 import select_autoescape

import numpy as np
from csv import reader
import csv
env = Environment(
    loader=PackageLoader('app', 'templates') # wskazujemy w jakim projekcie pythonowym (app) i jakim folderze (templates) znajduje się template
    # autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template("template1.html")

file = open('app/static/data/pkw2000.csv')
my_reader = csv.reader(file)
plikDoPrzerobienia = list(my_reader)
plik = np.array(plikDoPrzerobienia)
dane = plik[1:, 11:]
osoby = plik[0][11:]

print(dane[0])
print(dane[0][5])
print(osoby[0])

tablica_sum = [0 for i in range(12)]


def oblicz_polska():
    tablica_sum = [0 for i in range(12)]
    for y in range(1, 2495):
        for x in range(12):
            tablica_sum[x] = tablica_sum[x] + int(plik[y][11+x])
    return tablica_sum

tablica_sum = [0 for i in range(13)]
suma = 0

def oblicz_liczbe_glosow(zasieg, nazwa_miejsca):

    global tablica_sum
    tablica_sum = [0 for i in range(12)]
    if zasieg == -1:
        for y in range(1, 2495):
            for x in range(12):
                tablica_sum[x] = tablica_sum[x] + int(plik[y][11 + x])
    return tablica_sum

def oblicz_sume():
    global tablica_sum
    global suma
    suma = 0
    for x in range(12):
        suma = suma + tablica_sum[x]
    return suma

template.globals['oblicz_polska'] = oblicz_polska()

with open("generated_output/output.html", "w") as out:
    out.write(
        template.render(
            # number=42,
            # string='abc',
            # collection=list(range(1, 7))
            suma_kolumn=[0, 0, 0],
            dane=dane,
            osoby=osoby,
            liczba_glosow_na_kandydata=oblicz_liczbe_glosow(-1, ''),
            suma_glosow=oblicz_sume()
        )
    )