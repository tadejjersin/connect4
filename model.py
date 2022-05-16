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
        if konec:
            print(f"Zmagal je igralec z barvo: {zmagovalec}")
            return True
        else:
            return False
        


class Stanje():
    def __init__(self):
        self.trenutno_polje_za_2 = Polje()
        self.trenutno_polje_za_1 = Polje()
        self.trenutna_tema = 0

    
    def novo_polje_za_2(self):
        self.trenutno_polje_za_2 = Polje()
    
    def novo_polje_za_1(self):
        self.trenutno_polje_za_1 = Polje()

    def zamenjaj_temo(self):
        self.trenutna_tema = (self.trenutna_tema + 1) % 2

        
        