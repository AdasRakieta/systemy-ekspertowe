import rule_engine
import json
import datetime
from pathlib import Path 

def load_books_from_json(path):
    """
    Wczytuje plik JSON z bazą książek i konwertuje go
    do formatu kompatybilnego ze skryptem:
    rules = [(expr, points, explanation), ...]
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    books = []

    for b in data["books"]:
        converted_rules = []
        for rule in b["rules"]:
            expr = rule["condition"]
            pts = rule["points"]
            explanation = rule["description"]
            converted_rules.append((expr, pts, explanation))

        books.append({
            "name": b["name"],
            "rules": converted_rules
        })

    return books


# ------------------ Funkcje kontekstowe ------------------

def sugerowany_gatunek_dla_godziny():
    """
    Zwraca sugerowany gatunek książki w zależności od pory dnia.
    """
    godzina = datetime.datetime.now().hour
    if 5 <= godzina <= 9:
        return "biografia"  # rano - motywujące historie
    elif 10 <= godzina <= 14:
        return "reportaz"  # w ciągu dnia - poznawcze
    elif 15 <= godzina <= 18:
        return "thriller"  # popołudnie - angażujące
    elif 19 <= godzina <= 22:
        return "romans"  # wieczór - relaksujące
    else:
        return "horror"  # noc - mroczne


def sugerowany_klimat_dla_nastroju(nastroj):
    """
    Zwraca sugerowany klimat książki w zależności od nastroju czytelnika.
    """
    klimaty = {
        "dobry": "przygodowy",
        "zly": "mroczny",
        "neutralny": "realistyczny",
        "smutny": "refleksyjny",
        "radosny": "humorystyczny",
        "zestresowany": "relaksujacy"
    }
    return klimaty.get(nastroj, "realistyczny")


def szacowany_czas_czytania(dlugosc, tempo_czytania="srednie"):
    """
    Szacuje czas potrzebny na przeczytanie książki (w minutach).
    """
    bazowe_czasy = {
        "krotka": 180,      # 3h
        "srednia": 480,     # 8h
        "dluga": 900,       # 15h
        "bardzo_dluga": 1440  # 24h
    }
    
    czas = bazowe_czasy.get(dlugosc, 480)
    
    # Modyfikacja w zależności od tempa czytania
    if tempo_czytania == "wolne":
        czas = int(czas * 1.5)
    elif tempo_czytania == "szybkie":
        czas = int(czas * 0.7)
    
    return czas


def sugerowane_tempo_dla_czasu_wolnego(dostepny_czas):
    """
    Zwraca sugerowane tempo narracji w zależności od dostępnego czasu (w minutach).
    """
    if dostepny_czas < 60:
        return "dynamiczne"  # mało czasu - coś szybkiego
    elif dostepny_czas < 180:
        return "umiarkowane"  # trochę czasu
    else:
        return "powolne"  # dużo czasu - można spokojnie


def sugerowany_swiat_dla_pory_roku():
    """
    Zwraca sugerowany świat akcji w zależności od pory roku.
    """
    miesiac = datetime.datetime.now().month
    
    if miesiac in [12, 1, 2]:  # zima
        return "przyszlosc"  # sci-fi na zimowe wieczory
    elif miesiac in [3, 4, 5]:  # wiosna
        return "wspolczesnosc"  # coś bliskiego rzeczywistości
    elif miesiac in [6, 7, 8]:  # lato
        return "fantasy"  # magiczne przygody
    else:  # jesień (9, 10, 11)
        return "alternatywna_rzeczywistosc"  # inny wymiar


BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "KSIAZKI_BAZA.json"

books = load_books_from_json(json_path)


# ------------------ Konfiguracja rule_engine ------------------

# Słownik funkcji dostępnych w regułach
CUSTOM_FUNCTIONS = {
    "sugerowany_gatunek_dla_godziny": sugerowany_gatunek_dla_godziny,
    "sugerowany_klimat_dla_nastroju": sugerowany_klimat_dla_nastroju,
    "szacowany_czas_czytania": szacowany_czas_czytania,
    "sugerowane_tempo_dla_czasu_wolnego": sugerowane_tempo_dla_czasu_wolnego,
    "sugerowany_swiat_dla_pory_roku": sugerowany_swiat_dla_pory_roku,
}


def resolver(thing, name):
    """
    Resolver dla rule_engine - umożliwia dostęp do zmiennych i funkcji.
    """
    # Najpierw zmienne wejściowe (preferencje)
    if name in thing:
        return thing[name]
    
    # Następnie funkcje
    if name in CUSTOM_FUNCTIONS:
        return CUSTOM_FUNCTIONS[name]
    
    # Jeśli pola nie ma w preferencjach, zwróć None (reguła nie będzie pasować)
    return None


# Tworzymy kontekst rule_engine z naszym resolverem
context = rule_engine.Context(resolver=resolver)


# ------------------ Silnik wyboru książki ------------------


def wybierz_ksiazke(preferencje):
    ranking = []

    for book in books:
        score = 0
        reasons = []

        for expr, pts, explanation in book["rules"]:
            rule = rule_engine.Rule(expr, context=context)
            if rule.matches(preferencje):
                score += pts
                reasons.append(f"+{pts} pkt: {explanation}")

        ranking.append({
            "name": book["name"],
            "score": score,
            "reasons": reasons
        })

    ranking = sorted(ranking, key=lambda x: x["score"], reverse=True)

    top3 = ranking[:3]

    max_score = top3[0]["score"]
    explanations = [b for b in top3 if b["score"] == max_score]

    # generowanie wyjaśnień
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
    
    print("\n==================== TEST 1 — PROFIL PODSTAWOWY ====================\n")
    
    profil = {
        "gatunek": "reportaz",
        "klimat": "realistyczny",
        "dlugosc": "srednia",
        "tempo": "dynamiczne",
        "wiek_bohatera": "dorosly",
        "swiat": "przyszlosc",
        "miejsce": "miasto",
        "pochodzenie": "skandynawia",
        "epoka": "sredniowiecze"
    }
    
    wynik = wybierz_ksiazke(profil)
    
    print("TOP 3:\n")
    for p in wynik["top3"]:
        print(f"- {p['name']}: {p['score']} pkt")
    
    print("\nWYJAŚNIENIA:\n")
    print(wynik["wyjasnienia"])
    
    
    print("\n==================== TEST 2 — PROFIL Z GODZINĄ ====================\n")
    
    profil2 = {
        "gatunek": sugerowany_gatunek_dla_godziny(),
        "klimat": sugerowany_klimat_dla_nastroju("dobry"),
        "dlugosc": "srednia",
        "tempo": "dynamiczne",
        "wiek_bohatera": "dorosly",
        "swiat": sugerowany_swiat_dla_pory_roku(),
        "miejsce": "miasto",
    }
    
    print(f"Sugerowany gatunek dla tej godziny: {profil2['gatunek']}")
    print(f"Sugerowany klimat dla dobrego nastroju: {profil2['klimat']}")
    print(f"Sugerowany świat dla tej pory roku: {profil2['swiat']}\n")
    
    wynik2 = wybierz_ksiazke(profil2)
    
    print("TOP 3:\n")
    for p in wynik2["top3"]:
        print(f"- {p['name']}: {p['score']} pkt")
    
    print("\nWYJAŚNIENIA:\n")
    print(wynik2["wyjasnienia"])
    
    
    print("\n==================== TEST 3 — PROFIL Z CZASEM CZYTANIA ====================\n")
    
    dostepny_czas = 120  # 2 godziny
    
    profil3 = {
        "gatunek": "thriller",
        "klimat": "mroczny",
        "dlugosc": "srednia",
        "tempo": sugerowane_tempo_dla_czasu_wolnego(dostepny_czas),
        "wiek_bohatera": "dorosly",
    }
    
    czas_czytania = szacowany_czas_czytania(
        dlugosc="srednia",
        tempo_czytania="srednie"
    )
    
    print(f"Dostępny czas: {dostepny_czas} min")
    print(f"Sugerowane tempo: {profil3['tempo']}")
    print(f"Szacowany czas czytania książki: {czas_czytania} min (~{czas_czytania//60}h {czas_czytania%60}min)\n")
    
    wynik3 = wybierz_ksiazke(profil3)
    
    print("TOP 3:\n")
    for p in wynik3["top3"]:
        print(f"- {p['name']}: {p['score']} pkt")
    
    print("\nWYJAŚNIENIA:\n")
    print(wynik3["wyjasnienia"])
