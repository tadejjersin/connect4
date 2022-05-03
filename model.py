class Polje():
    def __init__(self):
        self.seznam_potez = []
        self.mreza = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
    
    def dodaj_potezo(self, igralec: str, stolpec: int):
        barva = None
        if igralec == "igralec1":
            barva = "R"
        elif igralec == "igralec2":
            barva = "M"
        
        vrstica = -1
        for i in self.mreza:
            if i[stolpec] != 0:
                break
            vrstica += 1

        if vrstica != -1:
            self.mreza[vrstica][stolpec] = barva
            self.seznam_potez.append((barva, vrstica, stolpec))
        else:
            return 

    def preveri_zmago(self):
        zmagovalec = None
        
        for vrstica in range(6): # treba še napisat pomožne funkcije
            for stolpec in range(7):
                if vrstica < 3:
                    preveri_stolpec(self.mreza, vrstica, stolpec)
                    if stolpec < 4:
                        preveri_diagonalo1(self.mreza, vrstica, stolpec)
                if stolpec < 4:
                    preveri_vrstico(self.mreza, vrstica, stolpec)
                    if vrstica >= 3:
                        preveri_diagonalo2(self.mreza, vrstica, stolpec)


class Stanje():
    def __init__(self):
        self.trenutno_polje = None
    
    def novo_polje(self):
        self.trenutno_polje = Polje()
                
        

        