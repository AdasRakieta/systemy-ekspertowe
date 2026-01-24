from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import rule_engine
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Umożliwia komunikację między frontendem a backendem

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "KSIAZKI_BAZA.json"


def load_books_from_json(path):
    """
    Wczytuje plik JSON z bazą książek i konwertuje go
    do formatu kompatybilnego ze skryptem
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


def wybierz_ksiazke(preferencje):
    """
    Silnik wyboru książki na podstawie preferencji użytkownika
    """
    books = load_books_from_json(JSON_PATH)
    ranking = []

    for book in books:
        score = 0
        reasons = []

        for expr, pts, explanation in book["rules"]:
            try:
                rule = rule_engine.Rule(expr)
                if rule.matches(preferencje):
                    score += pts
                    reasons.append(f"+{pts} pkt: {explanation}")
            except Exception as e:
                # Ignoruj błędy w regułach, które nie mają wymaganych pól
                continue

        ranking.append({
            "name": book["name"],
            "score": score,
            "reasons": reasons
        })

    ranking = sorted(ranking, key=lambda x: x["score"], reverse=True)
    top3 = ranking[:3]

    max_score = top3[0]["score"] if top3 else 0
    explanations = [b for b in top3 if b["score"] == max_score]

    return {
        "top3": top3,
        "winners": explanations,
        "all_results": ranking
    }


@app.route('/')
def index():
    """Strona główna - serwuje GUI"""
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """Serwuje pliki statyczne (CSS, JS)"""
    return send_from_directory('.', filename)


@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    Endpoint do rekomendacji książek
    Przyjmuje JSON z preferencjami użytkownika
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Brak danych wejściowych"}), 400
        
        # Walidacja - sprawdzamy czy są jakieś preferencje
        if not any(data.values()):
            return jsonify({"error": "Musisz wybrać przynajmniej jedną preferencję"}), 400
        
        result = wybierz_ksiazke(data)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/options', methods=['GET'])
def get_options():
    """
    Zwraca dostępne opcje dla każdego pola w formularzu
    """
    options = {
        "gatunek": [
            "fantasy", "kryminal", "romans", "biografia", "science_fiction",
            "historyczna", "thriller", "podroznicza", "obyczajowa", "horror",
            "mlodziezowa", "esej", "reportaz", "przygodowa", "satyra",
            "postapo", "detektywistyczna", "fakt", "groza", "komiks", "poezja"
        ],
        "klimat": [
            "mroczny", "lekki", "inspirujacy", "refleksyjny", "epicki",
            "psychologiczny", "przygodowy", "realistyczny", "gotycki",
            "humorystyczny", "tajemniczy", "dynamiczny", "liryczny"
        ],
        "dlugosc": [
            "krotka", "srednia", "dluga", "bardzo_dluga"
        ],
        "tempo": [
            "wolne", "umiarkowane", "dynamiczne"
        ],
        "wiek_bohatera": [
            "mlody", "dorosly", "starszy", "brak"
        ],
        "swiat": [
            "magiczny", "przyszlosc", "wspolczesny"
        ],
        "miejsce": [
            "miasto", "wies", "swiat", "las", "zamek", "szkola", "dzungla", "europa"
        ],
        "pochodzenie": [
            "skandynawia", "europa", "azja"
        ],
        "epoka": [
            "sredniowiecze", "wspolczesna", "przyszlosc"
        ]
    }
    return jsonify(options)


if __name__ == '__main__':
    print("🚀 Uruchamianie serwera backendu...")
    print("📚 System Ekspercki - Rekomendacja Książek")
    print("🌐 Serwer dostępny na: http://localhost:5001")
    print("📖 Otwórz przeglądarkę i wejdź na: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
