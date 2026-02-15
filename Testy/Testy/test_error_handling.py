import pytest

from Kawa_silnik import load_coffees_from_json, wybierz_kawe


class TestErrorHandling:

    """Testy obsługi błędów i wyjątków"""

    def test_missing_json_file(self):

        """Plik JSON nie istnieje"""

        with pytest.raises(FileNotFoundError):

            load_coffees_from_json("/nonexistent/path/kawy.json")

    def test_invalid_json_syntax(self, tmp_path):

        """Uszkodzony JSON (invalid syntax)"""

        json_file = tmp_path / "invalid.json"

        json_file.write_text("{invalid json,,,}")

        

        with pytest.raises(Exception):

            load_coffees_from_json(str(json_file))

    def test_json_missing_required_fields(self, tmp_path):

        """JSON brakuje wymaganych pól"""

        json_file = tmp_path / "incomplete.json"

        json_file.write_text('{"wrong_key": []}')

        

        with pytest.raises((KeyError, ValueError)):

            load_coffees_from_json(str(json_file))

    def test_rule_syntax_error_in_json(self, tmp_path):

        """Nieprawidłowa składnia warunku w regułach"""

        json_file = tmp_path / "bad_rule.json"

        bad_json = '''

        {

            "coffees": [{

                "name": "BadCoffee",

                "rules": [{

                    "condition": "moc === 'wysoka'",

                    "points": 10,

                    "description": "Bad"

                }]

            }]

        }

        '''

        json_file.write_text(bad_json)

        

        with pytest.raises(Exception):

            coffees = load_coffees_from_json(str(json_file))

    def test_encoding_error_with_special_chars(self, tmp_path):

        """Problemy z encoding polskich znaków"""

        json_file = tmp_path / "encoding_test.json"

        

        proper_json = '''

        {

            "coffees": [{

                "name": "Espresso",

                "rules": [{"condition": "moc == 'wysoka'", "points": 10, "description": "Bardzo mocna"}]

            }]

        }

        '''

        json_file.write_text(proper_json, encoding="utf-8")

        

        coffees = load_coffees_from_json(str(json_file))

        assert coffees[0]["name"] == "Espresso"
