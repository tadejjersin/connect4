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

@bottle.get("/igra1")
def igra():
    return "<p>namaanam</p>"

bottle.run(reloader=True, debug=True)