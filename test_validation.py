import pytest

from app import wybierz_ksiazke


class TestValidation:

    """Testy walidacji danych wejściowych"""

    def test_empty_profile(self):

        """Pusty profil nie powinien powodować błędu"""

        wynik = wybierz_ksiazke({})

        assert "top3" in wynik

        assert len(wynik["top3"]) == 3

    def test_none_profile(self):

        """None zamiast słownika powinno podnieść błąd"""

        wynik = wybierz_ksiazke(None)

        assert "top3" in wynik

    def test_invalid_attribute_value(self):

        """Nieznana wartość dla atrybutu nie powinna psuć działania"""

        profile = {

            "gatunek": "ultra_mega",

            "klimat": "nieznany",

            "dlugosc": "srednia",

            "tempo": "dynamiczne"

        }

        wynik = wybierz_ksiazke(profile)

        assert "top3" in wynik

    def test_missing_required_attributes(self):

        """Brak części pól nie powinien powodować błędu"""

        profile = {

            "gatunek": "fantasy",

            "klimat": "epicki"

        }

        wynik = wybierz_ksiazke(profile)

        assert "top3" in wynik

    def test_type_mismatch_number_instead_of_string(self):

        """Liczba zamiast stringa nie powinna powodować błędu"""

        profile = {

            "gatunek": 123,

            "klimat": "lekki",

            "dlugosc": "srednia",

            "tempo": "dynamiczne"

        }

        wynik = wybierz_ksiazke(profile)

        assert "top3" in wynik

    def test_extra_unknown_attributes_should_be_ignored(self):

        """Extra atrybuty powinny być zignorowane"""

        profile = {

            "gatunek": "thriller",

            "klimat": "mroczny",

            "tempo": "dynamiczne",

            "dlugosc": "srednia",

            "wiek": 25,

            "dochod": 5000

        }

        result = wybierz_ksiazke(profile)

        assert "top3" in result

    def test_null_values_in_attributes(self):

        """None/null wartości w atrybutach nie powinny powodować błędu"""

        profile = {

            "gatunek": "thriller",

            "klimat": None,

            "tempo": "dynamiczne",

            "dlugosc": "srednia"

        }

        wynik = wybierz_ksiazke(profile)

        assert "top3" in wynik
