import numpy as np
#  Zmiana narazie wstęp czyli rozpisanie możliwości ruchu atomów i ich interakcji między sobą i otoczeniem

class Atomy:
    def __init__(self, pozycja, predkosc, masa, promien):
        self.pozycja = np.array(pozycja)  # Ostatnia pozycja atomu
        self.predkosc = np.array(predkosc)  # Ostatnia prędkość atomu
        self.masa = masa  # masa atmou
        self.promien = promien  # promień atomu
        self.v_w_czasie = (np.copy(self.predkosc))  # Zapisywanie wszystkich prędkości oraz pozycji w czasie
        self.p_w_czasie = (np.copy(self.pozycja))
        self.v_w_czasie_w = (np.linalg.norm(np.copy(self.predkosc)))

    def Ruch_atomu(self, krok):
        self.pozycja += krok * self.predkosc  # obliczanie następnego "kroku" atomu
        self.v_w_czasie.append(np.copy(self.predkosc))
        self.p_w_czasie.append(np.copy(self.pozycja))
        self.v_w_czasie_w.append(np.linalg.norm(np.copy(self.predkosc)))

    def Ruch_po_zderzeniu(self, atom, krok):  # obliczamy ruch po zderzeniu
        m1, m2 = self.masa, atom.masa
        r1, r2 = self.promien, atom.promien
        v1, v2 = self.predkosc, atom.predkosc
        p1, p2 = self.pozycja, atom.pozycja
        di = p2 - p1
        norm = np.linalg.norm(di)
        if norm - (r1 + r2) * 1.1 < krok * abs(np.dot(v1 - v2, di)) / norm:
            self.predkosc = v1 - 2 * m2 / (m1 + m2) * np.dot(v1 - v2, di) / (np.linalg.norm(di) ** 2.) * di
            atom.predkosc = v2 - 2 * m1 / (m1 + m2) * np.dot(v2 - v1, (-di)) / (np.linalg.norm(di) ** 2.) * (-di)

    def Odbicie_od_sciany(self, krok, rozmiar):
        r = self.promien
        v = self.predkosc
        p = self.pozycja
        scianax = krok * abs(np.dot(v, np.array([1, 0])))
        scianay = krok * abs(np.dot(v, np.array([0, 1])))
        if abs(p[0]) - r < scianax or abs(rozmiar - p[0]) - r < scianax:
            self.predkosc[0] *= -1
        if abs(p[1]) - r < scianay or abs(rozmiar - p[1]) - r < scianay:
            self.predkosc[1] *= -1

def roz1(lista, krok, rozmiar): # lista to liczba atomów w liscie którą stworze potem
    for atom1 in lista:
        atom1.Odbicie_od_sciany(krok, rozmiar)
        for atom2 in lista:
            if atom1 is not atom2:
                atom1.Ruch_po_zderzeniu(atom2, krok)

def roz2(lista, krok):
    for atom in lista:
        atom.Ruch_atomu(krok)

def Rozwiazanie(lista, krok, rozmiar):
    lista = roz1(lista, krok, rozmiar)
    lista = roz2(lista, krok)
    return lista
