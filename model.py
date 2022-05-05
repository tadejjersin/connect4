import ai_nasprotnik

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
        else:
            return 

    def preveri_zmago(self):
        konec, zmagovalec = ai_nasprotnik.konec_igre(self.mreza)
        if konec:
            print(f"Zmagal je igralec z barvo: {zmagovalec}")
            return True
        else:
            return False
        


class Stanje():
    def __init__(self):
        self.trenutno_polje = None
    
    def novo_polje(self):
        self.trenutno_polje = Polje()
                
        

        