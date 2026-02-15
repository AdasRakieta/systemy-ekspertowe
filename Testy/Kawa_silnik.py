import json
import rule_engine
import datetime
from pathlib import Path


# ------------------ Funkcje własne ------------------

def sugerowana_kofeina_dla_godziny():
    godzina = datetime.datetime.now().hour
    if 5 <= godzina <= 10:
        return "wysoka"
    elif 11 <= godzina <= 15:
        return "średnia"
    elif 16 <= godzina <= 20:
        return "niska"
    else:
        return "bardzo_niska"


def oblicz_koszt_kawy(baza_ceny, mleko_ml=0, syrop_ml=0, dodatki=None):
    cena = baza_ceny
    cena += mleko_ml * 0.02
    cena += syrop_ml * 0.05

    add_costs = {
        "bita_śmietana": 2.00,
        "kakao": 1.00,
        "czekolada": 1.50,
        "cynamon": 0.50,
        "proszek_matcha": 3.00
    }

    if dodatki:
        for d in dodatki:
            cena += add_costs.get(d, 0)

    return round(cena, 2)


def czas_przygotowania(metoda, liczba_shotów=1, spienianie_mleka=False):
    bazowe_czasy = {
        "espresso": 25,
        "aeropress": 90,
        "drip": 180,
        "cold_brew": 4 * 3600,
        "french_press": 240,
        "moka": 150
    }

    czas = bazowe_czasy.get(metoda, 60)

    if liczba_shotów > 1:
        czas += (liczba_shotów - 1) * 20

    if spienianie_mleka:
        czas += 30

    return czas

def sugerowana_moc_dla_wrazliwosci(wrazliwosc):
    """
    Zwraca sugerowaną moc kawy w zależności od wrażliwości osoby.
    """
    if wrazliwosc == "wysoka":
        # osoba szybko pobudzona — delikatniejsze kawy
        return "niska"
    elif wrazliwosc == "średnia":
        # umiarkowana reakcja
        return "średnia"
    elif wrazliwosc == "niska":
        # osoba odporna — można mocniejsze
        return "wysoka"
    else:
        # wartość domyślna gdy brak danych
        return "średnia"
    
def sugerowana_kofeina_dla_wrazliwosci(wrazliwosc):
    """
    Zwraca sugerowaną zawartość kofeiny w zależności od reakcji osoby.
    """
    if wrazliwosc == "wysoka":
        # osoba „wrażliwa na kofeinę”
        return "niska"
    elif wrazliwosc == "średnia":
        # normalna reakcja
        return "średnia"
    elif wrazliwosc == "niska":
        # niewrażliwa — może pić mocniejsze
        return "wysoka"
    else:
        return "średnia"

# ------------------ Wczytywanie JSON ------------------

def load_coffees_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["coffees"]

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "KAWY_BAZA.json"

coffees = load_coffees_from_json(JSON_PATH)



#  tu tworzymy słownik funkcji dostępnych w regułach
CUSTOM_FUNCTIONS = {
    "sugerowana_kofeina_dla_godziny": sugerowana_kofeina_dla_godziny,
    "oblicz_koszt_kawy": oblicz_koszt_kawy,
    "czas_przygotowania": czas_przygotowania,
    "sugerowana_moc_dla_wrazliwosc": sugerowana_moc_dla_wrazliwosci,
    "sugerowana_kofeina_dla_wrazliwosci": sugerowana_kofeina_dla_wrazliwosci,
}


# poprwany resolver: musi mieć 3 argumenty: (thing, name, scope)
def resolver(thing, name):
    # najpierw zmienne wejściowe (preferencje)
    if name in thing:
        return thing[name]

    # następnie funkcje
    if name in CUSTOM_FUNCTIONS:
        return CUSTOM_FUNCTIONS[name]

    raise KeyError(name)


# tworzymy Kontext
context = rule_engine.Context(resolver=resolver)


# ------------------ SILNIK WYBORU KAWY ------------------

def wybierz_kawe(preferencje):
    ranking = []

    for coffee in coffees:
        score = 0
        reasons = []

        for rule_data in coffee["rules"]:
            expr = rule_data["condition"]
            pts = rule_data["points"]
            explanation = rule_data["description"]

            rule = rule_engine.Rule(expr, context=context)
            if rule.matches(preferencje):
                score += pts
                reasons.append(f"+{pts} pkt: {explanation}")

        ranking.append({
            "name": coffee["name"],
            "score": score,
            "reasons": reasons
        })

    ranking = sorted(ranking, key=lambda x: x["score"], reverse=True)
    top3 = ranking[:3]

    max_score = top3[0]["score"]
    explanations = [c for c in top3 if c["score"] == max_score]

    wyjasnienia = ""
    for e in explanations:
        wyjasnienia += f"\nWyjaśnienie dla **{e['name']}**:\n"
        for r in e["reasons"]:
            wyjasnienia += f"  • {r}\n"

    return {
        "top3": top3,
        "wyjasnienia": wyjasnienia
    }


# ------------------ TEST DZIAŁANIA ------------------

if __name__ == "__main__":

    print("\n==================== TEST 1 — PROFIL Z GODZINĄ ====================\n")

    profil = {
        "moc": "wysoka",
        "mleko": "brak",
        "slodycz": "niska",
        "wielkosc": "srednia",
        "temperatura": "gorąca",
        "kofeina": sugerowana_kofeina_dla_godziny(),
    }

    wynik = wybierz_kawe(profil)

    print("TOP 3:")
    for p in wynik["top3"]:
        print(f"- {p['name']} : {p['score']} pkt")

    print("\nWYJAŚNIENIA:")
    print(wynik["wyjasnienia"])
    print("\n==================== TEST 2 — PROFIL Z CZASEM PRZYGOTOWANIA ====================\n")

    czas = czas_przygotowania(
        metoda="espresso",
        liczba_shotów=2,
        spienianie_mleka=True
    )

    profil3 = {
        "moc": "bardzo wysoka",
        "mleko": "mało",
        "slodycz": "niska",
        "wielkosc": "mala",
        "temperatura": "gorąca",
        "kofeina": sugerowana_kofeina_dla_godziny(),
        "czas_przygotowania": czas
    }

    print(f"Szacowany czas przygotowania: {czas} sek.\n")

    wynik3 = wybierz_kawe(profil3)

    print("TOP 3:\n")
    for p in wynik3["top3"]:
        print(f"- {p['name']}: {p['score']} pkt")

    print("\nWYJAŚNIENIA:\n")
    print(wynik3["wyjasnienia"])

    print("\n==================== TEST 3 — PROFIL Z CZASEM PRZYGOTOWANIA ====================\n")


    profil4 = {
    "moc": sugerowana_moc_dla_wrazliwosci("wysoka"),
    "kofeina": sugerowana_moc_dla_wrazliwosci("wysoka"),
    "mleko": "mało",
    "slodycz": "niska",
    "temperatura": "gorąca",
    "wielkosc": "srednia"
}

    wynik4 = wybierz_kawe(profil4)

    print("TOP 3:\n")
    for p in wynik4["top3"]:
        print(f"- {p['name']}: {p['score']} pkt")

    print("\nWYJAŚNIENIA:\n")
    print(wynik4["wyjasnienia"])