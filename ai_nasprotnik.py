import math

def mozne_nove_mreze(mreza, igralec):
    if igralec:
        barva = "R"
    else:
        barva = "M"
    
    mreze_s_stolpci = []
    for stolpec in range(7):
        if mreza[0][stolpec] not in ["R", "M"]:
            nova_mreza = [v[:] for v in mreza]
            vrstica = [v[stolpec] for v in mreza].count("0") - 1
            nova_mreza[vrstica][stolpec] = barva
            mreze_s_stolpci.append((stolpec, nova_mreza))
    return mreze_s_stolpci


def konec_igre(mreza):
    if mreza[0].count("0") == 0: # če je prva vrstica polna je cela mreža polna
         return (True, None)
    kombinacije = mozne_kombinacije(mreza)
    for kombinacija in kombinacije:
        if kombinacija == "RRRR":
            return (True, "R")
        elif kombinacija == "MMMM":
            return (True, "M")
    else:
        return (False, None)

def vrednost_mreze(mreza):
    vrednost = 0
    mozne_komb = mozne_kombinacije(mreza)
    for kombinacija in mozne_komb:
        vrednost += doloci_vrednost_kombinacije(kombinacija)
    return vrednost

def mozne_kombinacije(mreza):
    kombinacije = []
    for vrstica in range(6): 
            for stolpec in range(7):
                if vrstica < 3:
                    kombinacija = ""
                    for i in range(4):
                        kombinacija += mreza[vrstica + i][stolpec]
                    kombinacije.append(kombinacija)
                    if stolpec < 4:
                        kombinacija = ""
                        for i in range(4):
                            kombinacija += mreza[vrstica + i][stolpec + i]
                        kombinacije.append(kombinacija)
                if stolpec < 4:
                    kombinacija = ""
                    for i in range(4):
                        kombinacija += mreza[vrstica][stolpec + i]
                    kombinacije.append(kombinacija)
                    if vrstica >= 3:
                        kombinacija = ""
                        for i in range(4):
                            kombinacija += mreza[vrstica - i][stolpec + i]
                        kombinacije.append(kombinacija)
    return kombinacije

def doloci_vrednost_kombinacije(kombinacija: str):
    stevilo_praznih = kombinacija.count("0")
    stevilo_rdecih = kombinacija.count("R")
    stevilo_modrih = kombinacija.count("M")
    if stevilo_praznih in [4, 3]:
        return 0
    elif stevilo_praznih == 2:
        if stevilo_modrih == 2:
            return -3
        else:
            return 0
    elif stevilo_praznih == 1:
        if stevilo_modrih == 3:
            return -10
        elif stevilo_rdecih == 3:
            return 7
        else:
            return 0
    else:
        if stevilo_modrih == 4:
            return -1000000
        elif stevilo_rdecih == 4:
            return 1000000
        else:
            return 0
        
# minimax algoritem
def minimax(mreza, globina, alpha, beta, igralec): # računalnik hoče čim manjši rezultat, igralec pa čim večjega
    if globina == 0 or konec_igre(mreza)[0]: 
        return (vrednost_mreze(mreza), None)

    if igralec:
        maksimalna_ocena = -math.inf
        for stolpec, nova_mreza in mozne_nove_mreze(mreza, True): 
            ocena = minimax(nova_mreza, globina - 1, alpha, beta, False)[0]
            nova_maksimalna_ocena = max(maksimalna_ocena, ocena)
            if nova_maksimalna_ocena > maksimalna_ocena:
                st = stolpec 
            maksimalna_ocena = nova_maksimalna_ocena
            alpha = max(alpha, ocena)
            if beta <= alpha:
                break
        return (maksimalna_ocena, st)
    
    else: 
        minimalna_ocena = math.inf
        for stolpec, nova_mreza in mozne_nove_mreze(mreza, False): 
            ocena = minimax(nova_mreza, globina - 1, alpha, beta, True)[0]
            nova_minimalna_ocena = min(minimalna_ocena, ocena)
            if nova_minimalna_ocena < minimalna_ocena:
                st = stolpec 
            minimalna_ocena = nova_minimalna_ocena
            beta = min(beta, ocena)
            if beta <= alpha:
                break
        return (minimalna_ocena, st)


