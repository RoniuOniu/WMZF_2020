import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class Atomy:
    def __init__(self, masa, promien, pozycja, predkosc):
        self.masa = masa
        self.promien = promien
        self.pozycja = np.array(pozycja)
        self.predkosc = np.array(predkosc)
        self.pozycja_w_cz = [np.copy(self.pozycja)]
        self.predkosc_w_cz = [np.copy(self.predkosc)]
        self.predkosc_w_cz_w = [np.linalg.norm(np.copy(self.predkosc))]

    def Ruch(self, krok):
        self.pozycja += krok * self.predkosc
        self.pozycja_w_cz.append(np.copy(self.pozycja))
        self.predkosc_w_cz.append(np.copy(self.predkosc))
        self.predkosc_w_cz_w.append(np.linalg.norm(np.copy(self.predkosc)))

    def Sprawdznie_kolizji(self, czastka):
        r1, r2 = self.promien, czastka.promien
        p1, p2 = self.pozycja, czastka.pozycja
        di = p2 - p1
        norm = np.linalg.norm(di)
        if norm - (r1 + r2) * 1.1 < 0:
            return True
        else:
            return False

    def Kolizja(self, czastka, krok):
        m1, m2 = self.masa, czastka.masa
        r1, r2 = self.promien, czastka.promien
        v1, v2 = self.predkosc, czastka.predkosc
        p1, p2 = self.pozycja, czastka.pozycja
        di = p2 - p1
        norm = np.linalg.norm(di)
        if norm - (r1 + r2) * 1.1 < krok * abs(np.dot(v1 - v2, di)) / norm:
            self.predkosc = v1 - 2. * m2 / (m1 + m2) * np.dot(v1 - v2, di) / (np.linalg.norm(di) ** 2.) * di
            czastka.predkosc = v2 - 2. * m1 / (m2 + m1) * np.dot(v2 - v1, (-di)) / (np.linalg.norm(di) ** 2.) * (-di)

    def Odbicie_od_sciany(self, krok, rozmiar):
        r, v, p = self.promien, self.predkosc, self.pozycja
        scianax = krok * abs(np.dot(v, np.array([1., 0.])))
        scianay = krok * abs(np.dot(v, np.array([0., 1.])))
        if abs(p[0]) - r < scianax or abs(rozmiar - p[0]) - r < scianax:
            self.predkosc[0] *= -1
        if abs(p[1]) - r < scianay or abs(rozmiar - p[1]) - r < scianay:
            self.predkosc[1] *= -1.

def Rozwiazanie(lista, krok, rozmiar):
    for i in range(len(lista)):
        lista[i].Odbicie_od_sciany(krok, rozmiar)
        for j in range(i + 1, len(lista)):
            lista[i].Kolizja(lista[j], krok)
    for czastka in lista:
        czastka.Ruch(krok)



def Random_list(N, promien, masa, pojemnik):
    lista = []
    for i in range(N):
        prędkość_p = np.random.rand(1) * 6
        prędkość_k = np.random.rand(1) * 2 * np.pi
        v = np.append(prędkość_p * np.cos(prędkość_k), prędkość_p * np.sin(prędkość_k))
        zderzenie = True
        while (zderzenie == True):
            zderzenie = False
            pos = promien + np.random.rand(2) * (pojemnik - 2 * promien)
            nowy_a = Atomy(masa, promien, pos, v)
            for j in range(len(lista)):
                zderzenie = nowy_a.Sprawdznie_kolizji(lista[j])
                if zderzenie == True:
                    break

        lista.append(nowy_a)
    return lista


liczba_atomow = 150
pojemnik = 400
czas = 30
liczba_krokow = 150
krok_czasu = czas / liczba_krokow
lista = Random_list(liczba_atomow, promien=4, masa=3, pojemnik=pojemnik)
for i in range(liczba_krokow):
    Rozwiazanie(lista, krok_czasu, pojemnik)


fig = plt.figure(figsize=(18, 8))
ax = fig.add_subplot(1, 2, 2)
hist = fig.add_subplot(1, 2, 1)
plt.subplots_adjust(bottom=0.2, left=0.1)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_xlim([0, pojemnik])
ax.set_ylim([0, pojemnik])
kolo = [None] * liczba_atomow
for i in range(liczba_atomow):
    kolo[i] = plt.Circle((lista[i].pozycja_w_cz[0][0], lista[i].pozycja_w_cz[0][1]), lista[i].promien,
                         ec="red", lw=0.5,zorder=20)
    ax.add_patch(kolo[i])
predkosc_m = [lista[i].predkosc_w_cz_w[0] for i in range(len(lista))]
hist.hist(predkosc_m, bins=20)
hist.set_xlabel("Prędkość")
hist.set_ylabel("liczba atomow")
suwak_ax = plt.axes([0.1, 0.05, 0.8, 0.05])
suwak = Slider(suwak_ax, 't', 0, czas,valinit=0)


def update(czas):
    i = int(np.rint(czas / krok_czasu))
    for j in range(liczba_atomow):
        kolo[j].center = lista[j].pozycja_w_cz[i][0], lista[j].pozycja_w_cz[i][1]
    hist.clear()
    predkosc_m = [lista[j].predkosc_w_cz_w[i] for j in range(len(lista))]
    hist.hist(predkosc_m, bins=20)
    hist.set_xlabel("Prędkość")
    hist.set_ylabel("Liczba atomow")

suwak.on_changed(update)
plt.show()

