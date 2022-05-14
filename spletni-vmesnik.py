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
        mreza = stanje.trenutno_polje_za_2.mreza
    )

@bottle.post("/vrzi_v_stolpec/<id_stolpca:int>/")
def vrzi_v_prvi_stolpec(id_stolpca):
    st = id_stolpca
    igralec = stanje.trenutno_polje_za_2.na_vrsti
    stanje.trenutno_polje_za_2.dodaj_potezo(igralec, st)
    bottle.redirect("/igra_za_dva")

bottle.run(reloader=True, debug=True)