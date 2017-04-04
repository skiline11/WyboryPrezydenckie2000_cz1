from jinja2 import Environment, PackageLoader
from jinja2 import select_autoescape
import numpy as np
from csv import reader
import csv

# Srodowisko
env = Environment(
    loader=PackageLoader('app', 'templates') # wskazujemy w jakim projekcie pythonowym (app) i jakim folderze (templates) znajduje się template
    # autoescape=select_autoescape(['html', 'xml'])
)

# Template'y
templateStrony = env.get_template("templateStrony.html")
# templateStrony.globals['oblicz_polska'] = oblicz_polska()
templateWykresuKolumnowego = env.get_template("templateWykresuKolumnowego.html")
templateStatystyki = env.get_template("templateStatystyki.html")

# Otwieram plik z danymi
file = open('app/static/data/pkw2000.csv')
my_reader = csv.reader(file)
plikDoPrzerobienia = list(my_reader)
plik = np.array(plikDoPrzerobienia)
dane = plik[1:, 11:]
osoby = plik[0][11:]

# Wypisuję dane kontrolnie
print(dane[0])
print(dane[0][5])
print(osoby[0])

def oblicz_polska():
    tablica_sum = [0 for i in range(12)]
    for y in range(1, 2495):
        for x in range(12):
            tablica_sum[x] += int(plik[y][11+x])
    return tablica_sum

tablica_sum = [0 for i in range(13)]
suma = 0


def oblicz_liczbe_glosow(zasieg, nazwa_miejsca):
    global tablica_sum
    tablica_sum = [0 for i in range(12)]
    if zasieg == -1:
        for y in range(1, 2495):
            for x in range(12):
                tablica_sum[x] += int(plik[y][11 + x])
    return tablica_sum


def oblicz_sume():
    global tablica_sum
    global suma
    suma = 0
    for x in range(12):
        suma += tablica_sum[x]
    return suma


def ilu_uprawnionych():
    liczba = 0
    for y in range(1, 2495):
        liczba += int(plik[y][6])
    return liczba


def oblicz_statystyki():
    ilu_uprawnionych = 0
    ile_kart_wydanych = 0
    ile_kart_wyjetych_z_urny = 0
    ile_glosow_waznych = 0
    for y in range(1, 2495):
        ilu_uprawnionych += int(plik[y][6])
        ile_kart_wydanych += int(plik[y][7])
        ile_kart_wyjetych_z_urny += int(plik[y][8])
        ile_glosow_waznych += int(plik[y][10])
    ile_glosow_niewaznych = ile_kart_wyjetych_z_urny - ile_glosow_waznych
    frekwencja = ile_kart_wydanych*100/ilu_uprawnionych
    statystyki = [ilu_uprawnionych, ile_kart_wydanych, ile_kart_wyjetych_z_urny, ile_glosow_waznych, ile_glosow_niewaznych, frekwencja]
    return statystyki


with open("generated_output/output.html", "w") as out:
    out.write(
        templateStrony.render(
            # number=42,
            # string='abc',
            # collection=list(range(1, 7))
            osoby=osoby,
            liczba_glosow_na_kandydata=oblicz_liczbe_glosow(-1, ''),
            suma_glosow=oblicz_sume(),
            uprawnieni=ilu_uprawnionych(),
            statystyki=oblicz_statystyki(),
        )
    )

with open("app/static/js/wykresKolumnowyPolska.js", "w") as out:
    out.write(
        templateWykresuKolumnowego.render(
            osoby=osoby,
            liczba_glosow_na_kandydata=oblicz_liczbe_glosow(-1, ''),
            suma_glosow=oblicz_sume()
        )
    )

def get_statystyki_ogolne():
    ostatnie = plik[1][0]
    ile_uprawnionych = int(plik[1][6])
    ile_wydanych_kart = int(plik[1][7])
    ile_wyjetych_kart = int(plik[1][8])
    ile_waznych_glosow = int(plik[1][9])
    ile_niewaznych_glosow = int(plik[1][10])
    frekwencja = 0
    wojewodztwa = []
    suma = [0 for i in range(7)]
    for y in range(2, 2495):
        if ostatnie != plik[y][0]:
            frekwencja = ile_wydanych_kart*100/ile_uprawnionych
            wojewodztwa.append([ostatnie, ile_uprawnionych, ile_wydanych_kart, ile_wyjetych_kart, ile_waznych_glosow, ile_niewaznych_glosow, frekwencja])
            suma[1] += ile_uprawnionych
            suma[2] += ile_wydanych_kart
            suma[3] += ile_wyjetych_kart
            suma[4] += ile_waznych_glosow
            suma[5] += ile_niewaznych_glosow
            ile_uprawnionych = 0
            ile_wydanych_kart = 0
            ile_wyjetych_kart = 0
            ile_waznych_glosow = 0
            ile_niewaznych_glosow = 0
        ile_uprawnionych += int(plik[y][6])
        ile_wydanych_kart += int(plik[y][7])
        ile_wyjetych_kart += int(plik[y][8])
        ile_niewaznych_glosow += int(plik[y][9])
        ile_waznych_glosow += int(plik[y][10])
        ostatnie = plik[y][0]
    suma[6] = suma[2] * 100 / suma[1]
    wyniki_wojewodztw = [suma, wojewodztwa]
    return wyniki_wojewodztw

with open("generated_output/statystykiOgolne.html", "w") as out:
    out.write(
        templateStatystyki.render(
            statystyki_ogolne=get_statystyki_ogolne(),
            typ_statystyk="Wojewodztwo"
        )
    )
