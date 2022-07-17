import ai_nasprotnik
import random
import math

class Polje():
    def __init__(self):
        self.seznam_potez = []
        self.mreza = [
            ["0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0"],
        ]
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
            self.seznam_potez.append((barva, vrstica, stolpec))
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
        
class Statistika():
    def __init__(self, igrane=0, izgubljene=0, zmagane=0, neodlocene=0):
        self.stevilo_igranih_iger = igrane
        self.stevilo_izgubljenih_iger = izgubljene
        self.stevilo_zmaganih_iger = zmagane
        self.stevilo_neodlocenih_iger = neodlocene
        self.seznam_hashov_koncanih_iger = set()

    def dodaj_igro(self, zmagovalec, igra): # -1 poraz , 0 neodloćeno, 1 zmaga
        self.seznam_hashov_koncanih_iger.add(igra)
        self.stevilo_igranih_iger += 1
        if zmagovalec == "R":
            self.stevilo_zmaganih_iger += 1
        elif zmagovalec == "M":
            self.stevilo_izgubljenih_iger += 1
        else:
            self.stevilo_neodlocenih_iger += 1
    

    def vrni_statistiko(self):
        return (self.stevilo_igranih_iger, self.stevilo_izgubljenih_iger, self.stevilo_zmaganih_iger, self.stevilo_neodlocenih_iger)
        

class Stanje():
    def __init__(self, igrane=0, izgubljene=0, zmagane=0, neodlocene=0):
        self.trenutno_polje_za_2 = Polje()
        self.trenutno_polje_za_1 = Polje()
        self.trenutna_tema = 0
        self.statistika = Statistika(igrane, izgubljene, zmagane, neodlocene)

    
    def novo_polje_za_2(self):
        self.trenutno_polje_za_2 = Polje()
    
    def novo_polje_za_1(self):
        self.trenutno_polje_za_1 = Polje()

    def zamenjaj_temo(self):
        self.trenutna_tema = (self.trenutna_tema + 1) % 2

        
        