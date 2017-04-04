from jinja2 import Environment, PackageLoader
from jinja2 import select_autoescape

import numpy as np
from csv import reader
import csv
env = Environment(
    loader=PackageLoader('app', 'templates') # wskazujemy w jakim projekcie pythonowym (app) i jakim folderze (templates) znajduje się template
    # autoescape=select_autoescape(['html', 'xml'])
)

file = open('app/static/data/pkw2000.csv')
my_reader = csv.reader(file)
plikDoPrzerobienia = list(my_reader)
plik = np.array(plikDoPrzerobienia)

def get_wojewodztwa():
    ostatnie = ''
    wojewodztwa = []
    for y in range(1, 2495):
        if ostatnie != plik[y][0]:
            ostatnie = plik[y][0]
            wojewodztwa.append(ostatnie)
    return wojewodztwa

woj=get_wojewodztwa()
print(woj)

tab = [2, 3, 4]
print(tab)

tab2 = [[0 for i in range(5)], [0 for i in range(5)]]
print(tab2[1])
