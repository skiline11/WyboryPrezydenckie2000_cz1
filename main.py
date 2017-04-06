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
templateStatystykiOgolne = env.get_template("templateStatystykiOgolne.html")

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


def get_statystyki_ogolne(indeks_x, nazwa):
    # 0 - typ statystyk - tabelka
    # 1 - uprawnionych do glosowania
    # 2 - wydanych kart
    # 3 - wyjetych kart
    # 4 - waznych glosow
    # 5 - niewaznych glosow
    # 6 - frekfencja
    uprawnionych = 0
    wydanych_kart = 0
    wyjetych_kart = 0
    niewaznych_glosow = 0
    waznych_glosow = 0
    for y in range(1, 2495):
        if indeks_x == -1 or plik[y][indeks_x] == nazwa:
            uprawnionych += int(plik[y][6])
            wydanych_kart += int(plik[y][7])
            wyjetych_kart += int(plik[y][8])
            niewaznych_glosow += int(plik[y][9])
            waznych_glosow += int(plik[y][10])
    frekwencja = wydanych_kart * 100 / uprawnionych
    wynik = [nazwa, uprawnionych, wydanych_kart, wyjetych_kart, niewaznych_glosow, waznych_glosow, frekwencja]
    return wynik


def get_statystyki_szczegolowe(indeks_x, nazwa, indeks_x2):
    statystyki = {}
    for y in range(1, 2495):
        if indeks_x == -1 or plik[y][indeks_x] == nazwa:
            if plik[y][indeks_x2] in statystyki:
                for a in range(5):
                    statystyki[plik[y][indeks_x2]][a + 1] += int(plik[y][a + 6])
                statystyki[plik[y][indeks_x2]][6] = float(statystyki[plik[y][indeks_x2]][2])*100.0/float(statystyki[plik[y][indeks_x2]][1])
            else:
                statystyki[plik[y][indeks_x2]] = [0, int(plik[y][6]), int(plik[y][7]), int(plik[y][8]), int(plik[y][9]), int(plik[y][10]), float(plik[y][7])*100.0/float(plik[y][6])]
    return statystyki

with open("generated_output/output.html", "w") as out:
    out.write(
        templateStrony.render(
            # number=42,
            # string='abc',
            # collection=list(range(1, 7))
            osoby=osoby,
            liczba_glosow_na_kandydata=oblicz_liczbe_glosow(-1, ''),
            suma_glosow=oblicz_sume()
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

with open("generated_output/statystykiOgolne.html", "w") as out:
    out.write(
        templateStatystykiOgolne.render(
            statystyki_ogolne=get_statystyki_ogolne(-1, ''),
            statystyki_szczegolowe=get_statystyki_szczegolowe(-1, 'a', 0),
            typ_statystyk="Wojewodztwo",
            czy_mapka=1
        )
    )
wojewodztwa = []
ost = ''
ile_wojewodztw = 0
for y in range(1, 2495):
    if plik[y][0] != ost:
        ost = plik[y][0]
        ile_wojewodztw += 1
        wojewodztwa.append(ost)
for x in range(ile_wojewodztw):
    with open("generated_output/statystyki" + wojewodztwa[x] + ".html", "w") as out:
        out.write(
            templateStatystykiOgolne.render(
                statystyki_ogolne=get_statystyki_ogolne(0, wojewodztwa[x]),
                statystyki_szczegolowe=get_statystyki_szczegolowe(0, wojewodztwa[x], 1),
                typ_statystyk="Okręg",
                czy_mapka=0
            )
        )


# with open("generated_output/statystykiMAZOWIECKIE.html", "w") as out:
#     out.write(
#         templateStatystykiOgolne.render(
#             statystyki_ogolne=get_statystyki_ogolne(0, 'MAZOWIECKIE'),
#             statystyki_szczegolowe=get_statystyki_szczegolowe(0, 'MAZOWIECKIE', 1),
#             typ_statystyk="Okręg"
#         )
#     )
