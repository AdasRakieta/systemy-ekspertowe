from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import rule_engine
import json
import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Umożliwia komunikację między frontendem a backendem

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "KSIAZKI_BAZA.json"


# ------------------ Funkcje własne ------------------

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
        return "wspolczesny"  # coś bliskiego rzeczywistości
    elif miesiac in [6, 7, 8]:  # lato
        return "magiczny"  # magiczne przygody
    else:  # jesień (9, 10, 11)
        return "historyczny"  # klasyczne klimaty


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


# ------------------ Ładowanie bazy książek ------------------


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
                rule = rule_engine.Rule(expr, context=context)
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
            "magiczny", "przyszlosc", "wspolczesny", "historyczny"
        ],
        "miejsce": [
            "miasto", "wies", "swiat", "las", "zamek", "szkola", "dzungla", "europa"
        ],
        "pochodzenie": [
            "skandynawia", "europa", "azja"
        ],
    }
    return jsonify(options)


@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """
    Zwraca sugestie bazujące na funkcjach kontekstowych
    (pora dnia, pora roku, itp.)
    """
    suggestions = {
        "gatunek": sugerowany_gatunek_dla_godziny(),
        "swiat": sugerowany_swiat_dla_pory_roku(),
        "klimat_dobry_nastroj": sugerowany_klimat_dla_nastroju("dobry"),
        "klimat_zly_nastroj": sugerowany_klimat_dla_nastroju("zły"),
        "tempo_malo_czasu": sugerowane_tempo_dla_czasu_wolnego(45),  # 45 min
        "tempo_duzo_czasu": sugerowane_tempo_dla_czasu_wolnego(240),  # 4h
        "godzina": datetime.datetime.now().hour,
        "miesiac": datetime.datetime.now().month,
    }
    return jsonify(suggestions)


@app.route('/api/reading-time', methods=['POST'])
def calculate_reading_time():
    """
    Oblicza szacowany czas czytania na podstawie długości i tempa
    """
    try:
        data = request.get_json()
        dlugosc = data.get('dlugosc', 'srednia')
        tempo = data.get('tempo_czytania', 'srednie')
        
        czas_min = szacowany_czas_czytania(dlugosc, tempo)
        
        return jsonify({
            "czas_minut": czas_min,
            "czas_godzin": round(czas_min / 60, 1),
            "opis": f"~{czas_min // 60}h {czas_min % 60}min"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🚀 Uruchamianie serwera backendu...")
    print("📚 System Ekspercki - Rekomendacja Książek")
    print("🌐 Serwer dostępny na: http://localhost:5001")
    print("📖 Otwórz przeglądarkę i wejdź na: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
