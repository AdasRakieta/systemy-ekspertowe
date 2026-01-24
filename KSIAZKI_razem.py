import rule_engine
import json
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


BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "KSIAZKI_BAZA.json"

books = load_books_from_json(json_path)

# Silnik wyboru książki


def wybierz_ksiazke(preferencje):
    ranking = []

    for book in books:
        score = 0
        reasons = []

        for expr, pts, explanation in book["rules"]:
            rule = rule_engine.Rule(expr)
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


# Przykład użycia - profil testowy z 3 setkami

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
