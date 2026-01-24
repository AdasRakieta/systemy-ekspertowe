import rule_engine
import json
from pathlib import Path

def load_coffees_from_json(path):
    """
    Wczytuje plik JSON z bazą kaw i konwertuje go
    do formatu kompatybilnego ze skryptem:
    rules = [(expr, points, explanation), ...]
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    coffees = []

    for c in data["coffees"]:
        converted_rules = []
        for rule in c["rules"]:
            expr = rule["condition"]
            pts = rule["points"]
            explanation = rule["description"]
            converted_rules.append((expr, pts, explanation))

        coffees.append({
            "name": c["name"],
            "rules": converted_rules
        })

    return coffees


BASE_DIR = Path(__file__).resolve().parent
json_path = BASE_DIR / "KAWY_BAZA.json"

coffees = load_coffees_from_json(json_path)

# Silnik wyboru kawy


def wybierz_kawe(preferencje):
    ranking = []

    for coffee in coffees:
        score = 0
        reasons = []

        for expr, pts, explanation in coffee["rules"]:
            rule = rule_engine.Rule(expr)
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


# Przykład użycia

profil = {
    "moc": "bardzo wysoka",
    "mleko": "brak",
    "slodycz": "niska",
    "wielkosc": "srednia",
    "temperatura": "gorąca",
    "kofeina": "wysoka"
}

wynik = wybierz_kawe(profil)

print("TOP 3:\n")
for p in wynik["top3"]:
    print(f"- {p['name']}: {p['score']} pkt")

print("\nWYJAŚNIENIA:\n")
print(wynik["wyjasnienia"])
