import pytest

from Kawa_silnik import wybierz_kawe


class TestValidation:

    """Testy walidacji danych wejściowych"""

    def test_empty_profile(self):

        """Pusty profil powinien zwrócić błąd"""

        with pytest.raises((ValueError, KeyError, TypeError)):

            wybierz_kawe({})

    def test_none_profile(self):

        """None zamiast słownika"""

        with pytest.raises((ValueError, TypeError, AttributeError)):

            wybierz_kawe(None)

    def test_invalid_attribute_value(self):

        """Nieznana wartość dla atrybutu"""

        profile = {

            "moc": "ultra_mega_mocna",

            "mleko": "brak",

            "slodycz": "niska",

            "wielkosc": "mala",

            "temperatura": "gorąca",

            "kofeina": "wysoka"

        }

        with pytest.raises((ValueError, KeyError)):

            wybierz_kawe(profile)

    def test_missing_required_attributes(self):

        """Brak wymaganych atrybutów"""

        profile = {

            "moc": "wysoka",

            "mleko": "brak"

        }

        with pytest.raises((ValueError, KeyError)):

            wybierz_kawe(profile)

    def test_type_mismatch_number_instead_of_string(self):

        """Liczba zamiast stringa"""

        profile = {

            "moc": 123,

            "mleko": "brak",

            "slodycz": "niska",

            "wielkosc": "mala",

            "temperatura": "gorąca",

            "kofeina": "wysoka"

        }

        with pytest.raises((TypeError, ValueError)):

            wybierz_kawe(profile)

    def test_extra_unknown_attributes_should_be_ignored(self):

        """Extra atrybuty powinny być zignorowane"""

        profile = {

            "moc": "wysoka",

            "mleko": "brak",

            "slodycz": "niska",

            "wielkosc": "mala",

            "temperatura": "gorąca",

            "kofeina": "wysoka",

            "wiek": 25,

            "dochod": 5000

        }

        result = wybierz_kawe(profile)

        assert "top3" in result

    def test_null_values_in_attributes(self):

        """None/null wartości w atrybutach"""

        profile = {

            "moc": "wysoka",

            "mleko": None,

            "slodycz": "niska",

            "wielkosc": "mala",

            "temperatura": "gorąca",

            "kofeina": "wysoka"

        }

        with pytest.raises((TypeError, ValueError)):

            wybierz_kawe(profile)
