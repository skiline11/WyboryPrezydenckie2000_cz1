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

def get_okregi():
    numer_okregu = '1'
    nazwa_okregu = ''
    okregi = []
    for y in range(1, 2495):
        if plik[y][1] != numer_okregu:
            okregi.append([nazwa_okregu, numer_okregu])
            nazwa_okregu = ''
            numer_okregu = plik[y][1]
        if plik[y][3] == plik[y][4]:
            if nazwa_okregu == '':
                nazwa_okregu = plik[y][3]
    return okregi


# 0 - typ statystyk - tabelka
# 1 - uprawnionych do glosowania
# 2 - wydanych kart
# 3 - wyjetych kart
# 4 - waznych glosow
# 5 - niewaznych glosow
# 6 - frekfencja
def get_calosc(indeks_x, nazwa):
    uprawnionych = 0
    wydanych_kart = 0
    wyjetych_kart = 0
    niewaznych_glosow = 0
    waznych_glosow = 0
    for y in range(1, 2495):
        if plik[y][indeks_x] == nazwa or indeks_x == -1:
            uprawnionych += int(plik[y][6])
            wydanych_kart += int(plik[y][7])
            wyjetych_kart += int(plik[y][8])
            niewaznych_glosow += int(plik[y][9])
            waznych_glosow += int(plik[y][10])
    frekwencja = wydanych_kart * 100 / uprawnionych
    wynik = [nazwa, uprawnionych, wydanych_kart, wyjetych_kart, niewaznych_glosow, waznych_glosow, frekwencja]
    return wynik

indeks_x = -1
nazwa = plik[1][0]
tab = get_calosc(indeks_x, nazwa)
print(tab)

tral = {}
tral["e"] = [1, 2]
tral["a"] = [1, 2, 3]
tral["b"] = [2, 7]
tral["a"][1] += 10
x="a"
print(tral["a"])
for key, value in sorted(tral.items()):
    print(key, value)


def get_statystyki_szczegolowe(indeks_x, nazwa, indeks_x2):
    statystyki = {}
    for y in range(1, 2495):
        if indeks_x == -1 or plik[y][indeks_x] == nazwa:
            if plik[y][indeks_x2] in statystyki:
                for a in range(6):
                    statystyki[plik[y][indeks_x2]][a + 1] += int(plik[y][a + 6])
                statystyki[plik[y][indeks_x2]][6] = statystyki[plik[y][indeks_x2]][2]*100/statystyki[plik[y][indeks_x2]][1]
            else:
                statystyki[plik[y][indeks_x2]] = [0, int(plik[y][6]), int(plik[y][7]), int(plik[y][8]), int(plik[y][9]), int(plik[y][10]), int(plik[y][7])*100.0/int(plik[y][6])]
    return statystyki

statystyki_szczegolowe = get_statystyki_szczegolowe(-1, 'a', 0)
for key, value in sorted(statystyki_szczegolowe.items()):
    print(key, value[1])

print()


