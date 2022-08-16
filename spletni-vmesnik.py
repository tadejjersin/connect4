import bottle
import model

with open("skrivnost.txt") as f:
    SKRIVNOST = f.read()
vse_skupaj = model.VseSkupaj.preberi_iz_datoteke("stanje.json")


def shrani_stanje():
    vse_skupaj.shrani_v_datoteko("stanje.json")

def stanje_trenutnega_uporabnika():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST)
    if uporabnisko_ime is None:
        bottle.redirect("/prijava/")
    else:
        return vse_skupaj.poisci_uporabnika(uporabnisko_ime).stanje

@bottle.get("/prijava/")
def prijava_get():
    return bottle.template(
        "prijava.html",
        napaka=None
    )

@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    uporabnik = vse_skupaj.poisci_uporabnika(uporabnisko_ime, geslo_v_cistopisu)
    if uporabnik:
        bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.redirect("/")
    else:
        return bottle.template("prijava.html", napaka="Napačno geslo")

@bottle.get("/registracija")
def registracija_get():
    return bottle.template(
        "registracija.html",
        napaka=None
    )

@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    if vse_skupaj.poisci_uporabnika(uporabnisko_ime):
        return bottle.template("registracija.html", napaka="Uporabniško ime že obstaja")
    else:
        zasifrirano_geslo = model.Uporabnik.zasifriraj_geslo(geslo_v_cistopisu)
        uporabnik = model.Uporabnik(uporabnisko_ime, zasifrirano_geslo, model.Stanje())
        vse_skupaj.uporabniki.append(uporabnik)
        shrani_stanje()
        bottle.redirect("/")

@bottle.post("/ustvari_racun/")
def ustvari_racun():
    bottle.redirect("/registracija")

@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie("uporabnisko_ime", path="/", secret=SKRIVNOST)
    bottle.redirect("/")

@bottle.get("/")
def zacetni_zaslon():
    stanje = stanje_trenutnega_uporabnika()
    return bottle.template(
        "zacetni_zaslon.html",
        stanje=stanje,
        tema=stanje.trenutna_tema
        )

@bottle.route("/static/<filepath:path>")
def load_static(filepath):
    return bottle.static_file(filepath, root="./static")

@bottle.post("/zamenjaj_temo/")
def zamenjaj_temo():
    stanje = stanje_trenutnega_uporabnika()
    stanje.zamenjaj_temo()
    bottle.redirect("/")

@bottle.get("/igra_za_dva")
def igra1():
    stanje = stanje_trenutnega_uporabnika()
    naslednji = stanje.trenutno_polje_za_2.na_vrsti
    if naslednji == "igralec1":
        na_vrsti = "rdeči igralec"
        ni_na_vrsti = "zeleni igralec"
    else:
        na_vrsti = "zeleni igralec"
        ni_na_vrsti = "rdeči igralec"
    return bottle.template(
        "igra_za_dva.html",
        na_vrsti = na_vrsti,
        ni_na_vrsti = ni_na_vrsti,
        mreza = stanje.trenutno_polje_za_2.mreza,
        konec = stanje.trenutno_polje_za_2.preveri_zmago()[0]
    )

@bottle.post("/vrzi_v_stolpec/<id_stolpca:int>/")
def vrzi_v_prvi_stolpec(id_stolpca):
    stanje = stanje_trenutnega_uporabnika()
    st = id_stolpca
    igralec = stanje.trenutno_polje_za_2.na_vrsti
    konec = stanje.trenutno_polje_za_2.preveri_zmago()[0]
    if not konec:
        stanje.trenutno_polje_za_2.dodaj_potezo(igralec, st)
    shrani_stanje()
    bottle.redirect("/igra_za_dva")

@bottle.post("/nova_igra/")
def nova_igra2():
    stanje = stanje_trenutnega_uporabnika()
    stanje.novo_polje_za_2()
    shrani_stanje()
    bottle.redirect("/igra_za_dva")

@bottle.post("/nazaj_na_zacetno_stran/")
def nazaj_na_zacetno_stran():
    bottle.redirect("/")

@bottle.get("/igra_za_enega")
def igra_za_enega():
    stanje = stanje_trenutnega_uporabnika()
    na_vrsti = stanje.trenutno_polje_za_1.na_vrsti
    konec, zmagovalec = stanje.trenutno_polje_za_1.preveri_zmago()
    if na_vrsti == "igralec2" and not konec:
        stolpec = stanje.trenutno_polje_za_1.idealni_stolpec(5)
        stanje.trenutno_polje_za_1.dodaj_potezo("igralec2", stolpec)
    mreza = stanje.trenutno_polje_za_1.mreza
    na_vrsti = stanje.trenutno_polje_za_1.na_vrsti
    konec, zmagovalec = stanje.trenutno_polje_za_1.preveri_zmago()
    koncane_igre = stanje.statistika.seznam_koncanih_iger
    igra = stanje.trenutno_polje_za_1.zaporedna_stevilka
    if konec and igra not in koncane_igre:
        stanje.statistika.dodaj_igro(zmagovalec, igra)
    shrani_stanje()
    return bottle.template(
        "igra_za_enega.html", 
        na_vrsti = na_vrsti,
        mreza = mreza,
        konec = konec
    )

@bottle.post("/vrzi_v_stolpec2/<id_stolpca:int>/")
def vrzi_v_prvi_stolpec(id_stolpca):
    stanje = stanje_trenutnega_uporabnika()
    st = id_stolpca
    igralec = stanje.trenutno_polje_za_1.na_vrsti
    konec = stanje.trenutno_polje_za_1.preveri_zmago()[0]
    if not konec:
        stanje.trenutno_polje_za_1.dodaj_potezo("igralec1", st)
    shrani_stanje()
    bottle.redirect("/igra_za_enega")

@bottle.post("/nova_igra1/")
def nova_igra1():
    stanje = stanje_trenutnega_uporabnika()
    stanje.novo_polje_za_1()
    shrani_stanje()
    bottle.redirect("/igra_za_enega")

@bottle.get("/statistika")
def statistika():
    stanje = stanje_trenutnega_uporabnika()
    stat = stanje.statistika.vrni_statistiko()
    return bottle.template(
        "statistika.html",
        st_igr = stat[0],
        st_izg = stat[1], 
        st_zm = stat[2],
        st_neod = stat[3],
    )

bottle.run(reloader=True, debug=True)