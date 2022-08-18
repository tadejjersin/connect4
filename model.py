import ai_nasprotnik
import random
import math
import json
from typing import List
from dataclasses import dataclass

class Polje():
    def __init__(self, zaporedna_stevilka, mreza=None, na_vrsti=None):
        self.zaporedna_stevilka = zaporedna_stevilka
        if mreza:
            self.mreza = mreza
        else:
            self.mreza = [
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
        ]
        if na_vrsti:
            self.na_vrsti = na_vrsti
        else:
            self.na_vrsti = random.choice(["igralec1", "igralec2"])
    
    def dodaj_potezo(self, igralec: str, stolpec: int):
        barva = None
        if igralec == "igralec1":
            barva = "R"
        elif igralec == "igralec2":
            barva = "M"
        
        vrstica = -1
        for i in self.mreza:
            if i[stolpec] != "0":
                break
            vrstica += 1

        if vrstica != -1:
            self.mreza[vrstica][stolpec] = barva
            if igralec == "igralec1":
                self.na_vrsti = "igralec2"
            else:
                self.na_vrsti = "igralec1"
        else:
            return 

    def idealni_stolpec(self, globina, igralec=False):
        return ai_nasprotnik.minimax(self.mreza, globina, -math.inf, math.inf, igralec)[1]

    def preveri_zmago(self):
        konec, zmagovalec = ai_nasprotnik.konec_igre(self.mreza)
        return (konec, zmagovalec)

    def v_slovar(self):
        return {
            "zaporedna_stevilka": self.zaporedna_stevilka,
            "mreza": self.mreza,
            "na_vrsti": self.na_vrsti
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Polje(
            slovar["zaporedna_stevilka"],
            slovar["mreza"],
            slovar["na_vrsti"]
        )
    
        
class Statistika():
    def __init__(self, igrane=0, izgubljene=0, zmagane=0, neodlocene=0, seznam_koncanih=set()):
        self.stevilo_igranih_iger = igrane
        self.stevilo_izgubljenih_iger = izgubljene
        self.stevilo_zmaganih_iger = zmagane
        self.stevilo_neodlocenih_iger = neodlocene
        self.seznam_koncanih_iger = seznam_koncanih

    def dodaj_igro(self, zmagovalec, igra): # -1 poraz , 0 neodloćeno, 1 zmaga
        self.seznam_koncanih_iger.add(igra)
        self.stevilo_igranih_iger += 1
        if zmagovalec == "R":
            self.stevilo_zmaganih_iger += 1
        elif zmagovalec == "M":
            self.stevilo_izgubljenih_iger += 1
        else:
            self.stevilo_neodlocenih_iger += 1

    def v_slovar(self):
        return {
            "stevilo_igranih_iger": self.stevilo_igranih_iger,
            "stevilo_izgubljenih_iger": self.stevilo_izgubljenih_iger,
            "stevilo_zmaganih_iger": self.stevilo_zmaganih_iger,
            "stevilo_neodlocenih_iger": self.stevilo_neodlocenih_iger,
            "seznam_koncanih": list(self.seznam_koncanih_iger)
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Statistika(
            slovar["stevilo_igranih_iger"],
            slovar["stevilo_izgubljenih_iger"],
            slovar["stevilo_zmaganih_iger"],
            slovar["stevilo_neodlocenih_iger"],
            set(slovar["seznam_koncanih"])
        )
    

    def vrni_statistiko(self):
        return (self.stevilo_igranih_iger, self.stevilo_izgubljenih_iger, self.stevilo_zmaganih_iger, self.stevilo_neodlocenih_iger)
        

class Stanje():
    def __init__(self, stevilo_vseh_polj=2, polje1=Polje(0), polje2=Polje(1), statistika=Statistika()):
        self.stevilo_vseh_polj = stevilo_vseh_polj
        self.trenutno_polje_za_2 = polje2
        self.trenutno_polje_za_1 = polje1
        self.trenutna_tema = 0
        self.statistika = statistika

    
    def novo_polje_za_2(self):
        self.trenutno_polje_za_2 = Polje(self.stevilo_vseh_polj)
        self.stevilo_vseh_polj += 1
    
    def novo_polje_za_1(self):
        self.trenutno_polje_za_1 = Polje(self.stevilo_vseh_polj)
        self.stevilo_vseh_polj += 1

    def zamenjaj_temo(self):
        self.trenutna_tema = (self.trenutna_tema + 1) % 2

    def v_slovar(self):
        return {
            "stevilo_vseh_polj": self.stevilo_vseh_polj,
            "polje_za_1": self.trenutno_polje_za_1.v_slovar(),
            "polje_za_2": self.trenutno_polje_za_2.v_slovar(),
            "statistika": self.statistika.v_slovar()
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Stanje(
            slovar["stevilo_vseh_polj"], 
            Polje.iz_slovarja(slovar["polje_za_1"]),
            Polje.iz_slovarja(slovar["polje_za_2"]),
            Statistika.iz_slovarja(slovar["statistika"])
        )


class Uporabnik():
    def __init__(self, uporabnisko_ime, geslo, stanje):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = geslo
        self.stanje = stanje

    @staticmethod
    def zasifriraj_geslo(geslo_v_cistopisu):
        return "XXX" + geslo_v_cistopisu[::-1] + "XXX"

    def ima_geslo(self, geslo_v_cistopisu):
        return self.zasifriraj_geslo(geslo_v_cistopisu) == self.zasifrirano_geslo

    def nastavi_novo_geslo(self, geslo_v_cistopisu):
        self.zasifrirano_geslo = self.zasifriraj_geslo(geslo_v_cistopisu)

    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "stanje": self.stanje.v_slovar(),
        }

    @classmethod
    def iz_slovarja(cls, slovar):
        return cls(
            slovar["uporabnisko_ime"],
            slovar["zasifrirano_geslo"],
            Stanje.iz_slovarja(slovar["stanje"])
        )


@dataclass
class VseSkupaj():
    uporabniki: List[Uporabnik]

    def poisci_uporabnika(self, uporabnisko_ime, geslo_v_cistopisu=None):
        for uporabnik in self.uporabniki:
            if uporabnik.uporabnisko_ime == uporabnisko_ime:
                if geslo_v_cistopisu is None or uporabnik.ima_geslo(geslo_v_cistopisu):
                    return uporabnik

    def v_slovar(self):
        return {
            "uporabniki": [uporabnik.v_slovar() for uporabnik in self.uporabniki],
        }

    @classmethod
    def iz_slovarja(cls, slovar):
        return cls(
            uporabniki=[Uporabnik.iz_slovarja(sl) for sl in slovar["uporabniki"]]
        )

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as d:
            slovar = self.v_slovar()
            json.dump(slovar, d)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as d:
            slovar = json.load(d)
            return VseSkupaj.iz_slovarja(slovar)

primer_stanja = Stanje()
primer_vsega_skupaj = VseSkupaj(
    uporabniki=[
        Uporabnik(
            "test",
            Uporabnik.zasifriraj_geslo("geslo"),
            primer_stanja,
        )
    ]
)