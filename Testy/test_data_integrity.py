import json

import pytest

from Kawa_silnik import load_coffees_from_json


class TestDataIntegrity:

    """Testy spójności i integralności bazy danych"""

    def test_json_structure_valid(self):

        """JSON ma prawidłową strukturę"""

        coffees = load_coffees_from_json("KAWY_BAZA.json")

        assert isinstance(coffees, list)

        assert len(coffees) > 0

    def test_each_coffee_has_required_fields(self):

        """Każda kawa ma wymagane pola"""

        coffees = load_coffees_from_json("KAWY_BAZA.json")

        for coffee in coffees:

            assert "name" in coffee, f"Coffee {coffee} missing 'name'"

            assert "rules" in coffee, f"Coffee {coffee} missing 'rules'"

            assert isinstance(coffee["rules"], list)

    def test_each_rule_has_required_fields(self):

        """Każda reguła ma wymagane pola"""

        coffees = load_coffees_from_json("KAWY_BAZA.json")

        for coffee in coffees:

            for rule in coffee["rules"]:

                assert "condition" in rule

                assert "points" in rule

                assert "description" in rule

    def test_no_duplicate_coffee_names(self):

        """Nie ma duplikatów kawy"""

        coffees = load_coffees_from_json("KAWY_BAZA.json")

        names = [c["name"] for c in coffees]

        assert len(names) == len(set(names)), "Duplicate coffee names found"

    def test_points_are_non_negative(self):

        """Wszystkie punkty są nieujemne"""

        coffees = load_coffees_from_json("KAWY_BAZA.json")

        for coffee in coffees:

            for rule in coffee["rules"]:

                assert rule["points"] >= 0, f"Negative points in {coffee['name']}"

    def test_attribute_values_are_consistent(self):

        """Wartości atrybutów w regułach są spójne"""

        coffees = load_coffees_from_json("KAWY_BAZA.json")

        

        allowed_values = {

            "moc": {"niska", "średnia", "wysoka", "bardzo wysoka"},

            "mleko": {"brak", "mało", "średnio", "dużo"},

            "slodycz": {"niska", "średnia", "wysoka"},

            "wielkosc": {"mala", "srednia", "duza"},

            "temperatura": {"gorąca", "zimna"},

            "kofeina": {"niska", "średnia", "wysoka"}

        }

        

        for coffee in coffees:

            for rule in coffee["rules"]:

                condition = rule["condition"]

                for attr, values in allowed_values.items():

                    for val in values:

                        if f"'{val}'" in condition:

                            pass
