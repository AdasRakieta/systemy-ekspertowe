import pytest
import rule_engine

from app import load_books_from_json


class TestErrorHandling:

    """Testy obsługi błędów i wyjątków"""

    def test_missing_json_file(self):

        """Plik JSON nie istnieje"""

        with pytest.raises(FileNotFoundError):

            load_books_from_json("/nonexistent/path/ksiazki.json")

    def test_invalid_json_syntax(self, tmp_path):

        """Uszkodzony JSON (invalid syntax)"""

        json_file = tmp_path / "invalid.json"

        json_file.write_text("{invalid json,,,}")

        

        with pytest.raises(Exception):

            load_books_from_json(str(json_file))

    def test_json_missing_required_fields(self, tmp_path):

        """JSON brakuje wymaganych pól"""

        json_file = tmp_path / "incomplete.json"

        json_file.write_text('{"wrong_key": []}')

        

        with pytest.raises(KeyError):

            load_books_from_json(str(json_file))

    def test_rule_syntax_error(self):

        """Nieprawidłowa składnia warunku w regułach"""

        with pytest.raises(Exception):

            rule_engine.Rule("gatunek === 'fantasy'")
