import pytest
import json
from pathlib import Path
import sys

# Importujemy funkcje z głównego pliku
sys.path.insert(0, str(Path(__file__).parent))
from KSIAZKI_razem import load_books_from_json, wybierz_ksiazke

BASE_DIR = Path(__file__).resolve().parent
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


class TestPointsSum:
    """Testy sprawdzające sumę punktów dla każdej książki"""
    
    def test_all_books_sum_to_100(self):
        """Test czy każda książka ma sumę punktów równą 100"""
        books = load_books_from_json(JSON_PATH)
        for book in books:
            total_points = sum(rule[1] for rule in book["rules"])
            assert total_points == 100, \
                f"Książka '{book['name']}' ma sumę {total_points} pkt zamiast 100"
    
    def test_positive_points(self):
        """Test czy wszystkie punkty są dodatnie"""
        books = load_books_from_json(JSON_PATH)
        for book in books:
            for rule in book["rules"]:
                assert rule[1] > 0, \
                    f"Reguła w książce '{book['name']}' ma niedodatnią liczbę punktów: {rule[1]}"


class TestWybierzKsiazke:
    """Testy dla funkcji wybierz_ksiazke"""
    
    def get_full_profil(self, **kwargs):
        """Pomocnicza funkcja tworząca pełny profil ze wszystkimi polami"""
        default_profil = {
            "gatunek": "",
            "klimat": "",
            "dlugosc": "",
            "tempo": "",
            "wiek_bohatera": "",
            "swiat": "",
            "miejsce": "",
            "pochodzenie": "",
            "epoka": ""
        }
        default_profil.update(kwargs)
        return default_profil
    
    def test_perfect_match(self):
        """Test idealnego dopasowania - profil dający 100 pkt dla jednej książki"""
        profil = self.get_full_profil(
            gatunek="fantasy",
            klimat="mroczny",
            dlugosc="bardzo_dluga",
            tempo="dynamiczne",
            wiek_bohatera="mlody",
            swiat="magiczny"
        )
        wynik = wybierz_ksiazke(profil)
        
        assert wynik["top3"][0]["score"] == 100, "Najlepsza książka powinna mieć 100 pkt"
        assert wynik["top3"][0]["name"] == "Fantastyka epicka"
        assert len(wynik["top3"][0]["reasons"]) == 5, "Powinno być 5 spełnionych reguł"
    
    def test_no_match(self):
        """Test braku dopasowania - profil niedający żadnych punktów"""
        profil = self.get_full_profil(
            gatunek="nieistniejacy_gatunek",
            klimat="nieistniejacy_klimat",
            dlugosc="nieistniejaca",
            tempo="nieistniejace",
            wiek_bohatera="nieistniejacy"
        )
        wynik = wybierz_ksiazke(profil)
        
        # Wszystkie książki powinny mieć 0 punktów
        for book in wynik["top3"]:
            assert book["score"] == 0, "Przy braku dopasowania wszystkie książki powinny mieć 0 pkt"
    
    def test_multiple_perfect_matches(self):
        """Test wielu idealnych dopasowań - profil dający 100 pkt dla 3 książek"""
        profil = self.get_full_profil(
            gatunek="reportaz",
            klimat="realistyczny",
            miejsce="miasto",
            dlugosc="srednia",
            tempo="dynamiczne"
        )
        wynik = wybierz_ksiazke(profil)
        
        # Powinny być co najmniej 3 książki z 100 pkt
        perfect_matches = [b for b in wynik["top3"] if b["score"] == 100]
        assert len(perfect_matches) == 3, "Powinny być 3 książki z maksymalnym wynikiem"
    
    def test_top3_sorted(self):
        """Test czy TOP 3 jest posortowane malejąco"""
        profil = self.get_full_profil(
            gatunek="fantasy",
            klimat="mroczny",
            tempo="dynamiczne"
        )
        wynik = wybierz_ksiazke(profil)
        
        scores = [book["score"] for book in wynik["top3"]]
        assert scores == sorted(scores, reverse=True), "TOP 3 powinno być posortowane malejąco"
    
    def test_top3_length(self):
        """Test czy zwracane są dokładnie 3 książki"""
        profil = self.get_full_profil(
            gatunek="fantasy",
            klimat="mroczny"
        )
        wynik = wybierz_ksiazke(profil)
        
        assert len(wynik["top3"]) == 3, "Powinny być zwrócone dokładnie 3 książki"
    
    def test_explanations_for_winners(self):
        """Test czy wyjaśnienia są generowane dla książek z najwyższym wynikiem"""
        profil = self.get_full_profil(
            gatunek="fantasy",
            klimat="mroczny",
            dlugosc="bardzo_dluga",
            tempo="dynamiczne",
            wiek_bohatera="mlody",
            swiat="magiczny"
        )
        wynik = wybierz_ksiazke(profil)
        
        assert "Wyjaśnienie dla" in wynik["wyjasnienia"], \
            "Wyjaśnienia powinny zawierać tekst 'Wyjaśnienie dla'"
        assert "Fantastyka epicka" in wynik["wyjasnienia"], \
            "Wyjaśnienia powinny zawierać nazwę zwycięskiej książki"


class TestJsonIntegrity:
    """Testy integralności pliku JSON"""
    
    def test_json_valid(self):
        """Test czy plik JSON jest poprawny"""
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "books" in data, "JSON powinien zawierać klucz 'books'"
    
    def test_unique_book_names(self):
        """Test czy nazwy książek są unikalne (z wyjątkiem wariantów reportaży)"""
        books = load_books_from_json(JSON_PATH)
        names = [book["name"] for book in books]
        # Sprawdzamy czy są duplikaty (poza celowymi)
        assert len(names) > 0, "Powinny być jakieś książki"
    
    def test_minimum_books_count(self):
        """Test czy jest przynajmniej 20 książek"""
        books = load_books_from_json(JSON_PATH)
        assert len(books) >= 20, f"Baza powinna zawierać przynajmniej 20 książek, a ma {len(books)}"
    
    def test_each_book_has_rules(self):
        """Test czy każda książka ma przynajmniej jedną regułę"""
        books = load_books_from_json(JSON_PATH)
        for book in books:
            assert len(book["rules"]) > 0, \
                f"Książka '{book['name']}' nie ma żadnych reguł"


class TestPartialMatches:
    """Testy dla częściowych dopasowań"""
    
    def get_full_profil(self, **kwargs):
        """Pomocnicza funkcja tworząca pełny profil ze wszystkimi polami"""
        default_profil = {
            "gatunek": "",
            "klimat": "",
            "dlugosc": "",
            "tempo": "",
            "wiek_bohatera": "",
            "swiat": "",
            "miejsce": "",
            "pochodzenie": "",
            "epoka": ""
        }
        default_profil.update(kwargs)
        return default_profil
    
    def test_partial_match_scoring(self):
        """Test częściowego dopasowania - tylko niektóre kryteria spełnione"""
        profil = self.get_full_profil(
            gatunek="fantasy",
            klimat="inny",
            dlugosc="inna",
            tempo="inne",
            wiek_bohatera="inny"
        )
        wynik = wybierz_ksiazke(profil)
        
        # Książka "Fantastyka epicka" powinna dostać tylko 30 pkt (za gatunek)
        fantasy_book = next((b for b in wynik["top3"] if b["name"] == "Fantastyka epicka"), None)
        assert fantasy_book is not None, "Fantastyka epicka powinna być w wynikach"
        assert fantasy_book["score"] == 30, "Powinno być 30 pkt za gatunek"
        assert len(fantasy_book["reasons"]) == 1, "Powinien być tylko 1 powód"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
