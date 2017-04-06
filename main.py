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


def oblicz_liczbe_glosow(indeks_x, nazwa_miejsca):
    global tablica_sum
    tablica_sum = [0 for i in range(12)]

    if indeks_x == -1:
        for y in range(1, 2495):
            for x in range(12):
                tablica_sum[x] += int(plik[y][11 + x])
    else:
        for y in range(1, 2495):
            if plik[y][indeks_x] == nazwa_miejsca:
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

wojewodztwa = []
ost = ''
ile_wojewodztw = 0
for y in range(1, 2495):
    if plik[y][0] != ost:
        ost = plik[y][0]
        ile_wojewodztw += 1
        wojewodztwa.append(ost)

with open("generated_output/Polska.html", "w") as out:
    out.write(
        templateStrony.render(
            osoby=osoby,
            statystyki_kandydatow=oblicz_liczbe_glosow(-1, ''),
            statystyki_ogolne=get_statystyki_ogolne(-1, ''),
            statystyki_szczegolowe=get_statystyki_szczegolowe(-1, 'a', 0),
            typ_statystyk="Wojewodztwo",
            czy_mapka=1,
            suma_glosow=oblicz_sume(),
            nazwa_wykresu="Polska"
        )
    )

with open("app/static/js/wykresKolumnowy_Polska.js", "w") as out:
    out.write(
        templateWykresuKolumnowego.render(
            osoby=osoby,
            liczba_glosow_na_kandydata=oblicz_liczbe_glosow(-1, ''),
            suma_glosow=oblicz_sume(),
            nazwa_wykresu="Polska"
        )
    )

for x in range(ile_wojewodztw):
    with open("generated_output/statystyki_Wojewodztwo_" + wojewodztwa[x] + ".html", "w") as out:
        out.write(
            templateStrony.render(
                osoby=osoby,
                statystyki_kandydatow=oblicz_liczbe_glosow(0, wojewodztwa[x]),
                statystyki_ogolne=get_statystyki_ogolne(0, wojewodztwa[x]),
                statystyki_szczegolowe=get_statystyki_szczegolowe(0, wojewodztwa[x], 1),
                typ_statystyk="Okreg",
                czy_mapka=0,
                suma_glosow=oblicz_sume(),
                nazwa_wykresu="Wojewodztwo_"+wojewodztwa[x]
            )
        )
    with open("app/static/js/wykresKolumnowy_Wojewodztwo_" + wojewodztwa[x] + ".js", "w") as out:
        out.write(
            templateWykresuKolumnowego.render(
                osoby=osoby,
                liczba_glosow_na_kandydata=oblicz_liczbe_glosow(0, wojewodztwa[x]),
                suma_glosow=oblicz_sume(),
                nazwa_wykresu="Wojewodztwo_"+wojewodztwa[x]
            )
        )

okregi = []
ost = ''
ile_okregow = 0
for y in range(1, 2495):
    if plik[y][1] != ost:
        ost = plik[y][1]
        ile_okregow += 1
        okregi.append(ost)
for x in range(ile_okregow):
    with open("generated_output/statystyki_Okreg_" + okregi[x] + ".html", "w") as out:
        out.write(
            templateStrony.render(
                osoby=osoby,
                statystyki_kandydatow=oblicz_liczbe_glosow(1, okregi[x]),
                statystyki_ogolne=get_statystyki_ogolne(1, okregi[x]),
                statystyki_szczegolowe=get_statystyki_szczegolowe(1, okregi[x], 4),
                typ_statystyk="Powiat",
                czy_mapka=0,
                suma_glosow=oblicz_sume(),
                nazwa_wykresu="Okreg_" + okregi[x]
            )
        )
    with open("app/static/js/wykresKolumnowy_Okreg_" + okregi[x] + ".js", "w") as out:
        out.write(
            templateWykresuKolumnowego.render(
                osoby=osoby,
                liczba_glosow_na_kandydata=oblicz_liczbe_glosow(1, okregi[x]),
                suma_glosow=oblicz_sume(),
                nazwa_wykresu="Okreg_"+okregi[x]
            )
        )

powiaty = []
ost = ''
ile_powiatow = 0
for y in range(1, 2495):
    if plik[y][4] != ost:
        ost = plik[y][4]
        ile_powiatow += 1
        powiaty.append(ost)
for x in range(ile_powiatow):
    with open("generated_output/statystyki_Powiat_" + powiaty[x] + ".html", "w") as out:
        out.write(
            templateStrony.render(
                osoby=osoby,
                statystyki_kandydatow=oblicz_liczbe_glosow(4, powiaty[x]),
                statystyki_ogolne=get_statystyki_ogolne(4, powiaty[x]),
                statystyki_szczegolowe=get_statystyki_szczegolowe(4, powiaty[x], 3),
                typ_statystyk="Gmina",
                czy_mapka=0,
                suma_glosow=oblicz_sume(),
                nazwa_wykresu="Powiat_" + powiaty[x]
            )
        )
    with open("app/static/js/wykresKolumnowy_Powiat_" + powiaty[x] + ".js", "w") as out:
        out.write(
            templateWykresuKolumnowego.render(
                osoby=osoby,
                liczba_glosow_na_kandydata=oblicz_liczbe_glosow(4, powiaty[x]),
                suma_glosow=oblicz_sume(),
                nazwa_wykresu="Powiat_"+powiaty[x]
            )
        )




## To zrobię puźniej bo szkoda mi czasu na czekanie na renderowanie stron :-)
# gminy = []
# ost = ''
# ile_gmin = 0
# for y in range(1, 2495):
#     if plik[y][3] != ost:
#         ost = plik[y][3]
#         ile_gmin += 1
#         gminy.append(ost)
# for x in range(ile_powiatow):
#     with open("generated_output/statystyki_Gmina_" + gminy[x] + ".html", "w") as out:
#         out.write(
#             templateStatystykiOgolne.render(
#                 statystyki_ogolne=get_statystyki_ogolne(3, powiaty[x]),
#                 typ_statystyk="brak",
#                 czy_mapka=0
#             )
#         )