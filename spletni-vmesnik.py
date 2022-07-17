import bottle
import model

stanje = model.Stanje()

@bottle.get("/")
def zacetni_zaslon():
    return bottle.template(
        "zacetni_zaslon.html",
        tema=stanje.trenutna_tema
        )

@bottle.route("/static/<filepath:path>")
def load_static(filepath):
    return bottle.static_file(filepath, root="./static")

@bottle.post("/zamenjaj_temo/")
def zamenjaj_temo():
    stanje.zamenjaj_temo()
    bottle.redirect("/")

@bottle.get("/igra_za_dva")
def igra1():
    return bottle.template(
        "igra_za_dva.html",
        na_vrsti = stanje.trenutno_polje_za_2.na_vrsti,
        mreza = stanje.trenutno_polje_za_2.mreza,
        konec = stanje.trenutno_polje_za_2.preveri_zmago()
    )

@bottle.post("/vrzi_v_stolpec/<id_stolpca:int>/")
def vrzi_v_prvi_stolpec(id_stolpca):
    st = id_stolpca
    igralec = stanje.trenutno_polje_za_2.na_vrsti
    konec = stanje.trenutno_polje_za_2.preveri_zmago()[0]
    if not konec:
        stanje.trenutno_polje_za_2.dodaj_potezo(igralec, st)
    bottle.redirect("/igra_za_dva")

@bottle.post("/nova_igra/")
def nova_igra2():
    stanje.novo_polje_za_2()
    bottle.redirect("/igra_za_dva")

@bottle.post("/nazaj_na_zacetno_stran/")
def nazaj_na_zacetno_stran():
    bottle.redirect("/")

@bottle.get("/igra_za_enega")
def igra_za_enega():
    na_vrsti = stanje.trenutno_polje_za_1.na_vrsti
    konec, zmagovalec = stanje.trenutno_polje_za_1.preveri_zmago()
    if na_vrsti == "igralec2" and not konec:
        stolpec = stanje.trenutno_polje_za_1.idealni_stolpec(5)
        stanje.trenutno_polje_za_1.dodaj_potezo("igralec2", stolpec)
    mreza = stanje.trenutno_polje_za_1.mreza
    na_vrsti = stanje.trenutno_polje_za_1.na_vrsti
    konec, zmagovalec = stanje.trenutno_polje_za_1.preveri_zmago()
    koncane_igre = stanje.statistika.seznam_hashov_koncanih_iger
    igra = hash(stanje.trenutno_polje_za_1)
    if konec and igra not in koncane_igre:
        stanje.statistika.dodaj_igro(zmagovalec, igra)
        
    return bottle.template(
        "igra_za_enega.html", 
        na_vrsti = na_vrsti,
        mreza = mreza,
        konec = konec
    )

@bottle.post("/vrzi_v_stolpec2/<id_stolpca:int>/")
def vrzi_v_prvi_stolpec(id_stolpca):
    st = id_stolpca
    igralec = stanje.trenutno_polje_za_1.na_vrsti
    konec = stanje.trenutno_polje_za_1.preveri_zmago()[0]
    if not konec:
        stanje.trenutno_polje_za_1.dodaj_potezo("igralec1", st)
    bottle.redirect("/igra_za_enega")

@bottle.post("/nova_igra1/")
def nova_igra1():
    stanje.novo_polje_za_1()
    bottle.redirect("/igra_za_enega")

@bottle.get("/statistika")
def statistika():
    stat = stanje.statistika.vrni_statistiko()
    return bottle.template(
        "statistika.html",
        st_igr = stat[0],
        st_izg = stat[1], 
        st_zm = stat[2],
        st_neod = stat[3],
    )

bottle.run(reloader=True, debug=True)