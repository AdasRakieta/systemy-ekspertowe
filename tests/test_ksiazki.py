import json
from pathlib import Path

from app import load_books_from_json, wybierz_ksiazke


BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "KSIAZKI_BAZA.json"


class TestLoadBooksFromJson:
    """Testy dla funkcji load_books_from_json"""
    
    def test_load_books_success(self):
        """Test poprawnego wczytania pliku JSON"""
        books = load_books_from_json(JSON_PATH)
        assert len(books) > 0, "Baza książek nie powinna być pusta"
        assert isinstance(books, list), "Wynik powinien być listą"
    
    def test_book_structure(self):
        """Test struktury wczytanych książek"""
        books = load_books_from_json(JSON_PATH)
        for book in books:
            assert "name" in book, "Książka powinna mieć pole 'name'"
            assert "rules" in book, "Książka powinna mieć pole 'rules'"
            assert isinstance(book["rules"], list), "Reguły powinny być listą"
    
    def test_rule_structure(self):
        """Test struktury reguł"""
        books = load_books_from_json(JSON_PATH)
        for book in books:
            for rule in book["rules"]:
                assert len(rule) == 3, "Reguła powinna mieć 3 elementy (expr, pts, explanation)"
                expr, pts, explanation = rule
                assert isinstance(expr, str), "Wyrażenie powinno być stringiem"
                assert isinstance(pts, int), "Punkty powinny być liczbą całkowitą"
                assert isinstance(explanation, str), "Wyjaśnienie powinno być stringiem"


class TestWybierzKsiazke:
    """Testy dla funkcji wybierz_ksiazke"""
    
    def test_perfect_match(self):
        """Test idealnego dopasowania"""
        profil = {
            "gatunek": "fantasy",
            "dlugosc": "bardzo_dluga",
            "tempo": "dynamiczne",
            "wiek_bohatera": "mlody",
            "swiat": "magiczny"
        }
        wynik = wybierz_ksiazke(profil)
        
        assert wynik["top3"][0]["score"] == 100
        assert wynik["top3"][0]["name"] == "Władca Pierścieni - J.R.R. Tolkien"
        assert len(wynik["top3"][0]["reasons"]) == 5
    
    def test_multiple_perfect_matches(self):
        """Test wielu idealnych dopasowań"""
        profil = {
            "gatunek": "reportaz",
            "klimat": "realistyczny",
            "miejsce": "miasto",
            "dlugosc": "srednia",
            "tempo": "dynamiczne"
        }
        wynik = wybierz_ksiazke(profil)
        
        perfect_matches = [b for b in wynik["top3"] if b["score"] == 100]
        assert len(perfect_matches) == 3
    
    def test_top3_sorted(self):
        """Test czy TOP 3 jest posortowane malejąco"""
        profil = {
            "gatunek": "fantasy",
            "tempo": "dynamiczne"
        }
        wynik = wybierz_ksiazke(profil)
        
        scores = [book["score"] for book in wynik["top3"]]
        assert scores == sorted(scores, reverse=True)
    
    def test_explanations_for_winners(self):
        """Test czy wyjaśnienia są generowane dla książek z najwyższym wynikiem"""
        profil = {
            "gatunek": "fantasy",
            "dlugosc": "bardzo_dluga",
            "tempo": "dynamiczne",
            "wiek_bohatera": "mlody",
            "swiat": "magiczny"
        }
        wynik = wybierz_ksiazke(profil)
        
        assert "winners" in wynik
        assert any(
            w["name"] == "Władca Pierścieni - J.R.R. Tolkien" for w in wynik["winners"]
        )


class TestJsonIntegrity:
    """Testy integralności pliku JSON"""
    
    def test_json_valid(self):
        """Test czy plik JSON jest poprawny"""
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "books" in data, "JSON powinien zawierać klucz 'books'"
    
    def test_minimum_books_count(self):
        """Test czy jest przynajmniej 20 książek"""
        books = load_books_from_json(JSON_PATH)
        assert len(books) >= 20, f"Baza powinna zawierać przynajmniej 20 książek, a ma {len(books)}"
    
    def test_each_book_has_rules(self):
        """Test czy każda książka ma przynajmniej jedną regułę"""
        books = load_books_from_json(JSON_PATH)
        for book in books:
            assert len(book["rules"]) > 0, f"Książka '{book['name']}' nie ma żadnych reguł"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
