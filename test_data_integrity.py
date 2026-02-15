from pathlib import Path

from KSIAZKI_razem import load_books_from_json


BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "KSIAZKI_BAZA.json"


class TestDataIntegrity:

    """Testy spójności i integralności bazy danych"""

    def test_json_structure_valid(self):

        """JSON ma prawidłową strukturę"""

        books = load_books_from_json(JSON_PATH)

        assert isinstance(books, list)

        assert len(books) > 0

    def test_each_book_has_required_fields(self):

        """Każda książka ma wymagane pola"""

        books = load_books_from_json(JSON_PATH)

        for book in books:

            assert "name" in book, f"Book {book} missing 'name'"

            assert "rules" in book, f"Book {book} missing 'rules'"

            assert isinstance(book["rules"], list)

    def test_each_rule_has_required_fields(self):

        """Każda reguła ma wymagane pola"""

        books = load_books_from_json(JSON_PATH)

        for book in books:

            for rule in book["rules"]:

                assert len(rule) == 3

                expr, pts, description = rule

                assert isinstance(expr, str)

                assert isinstance(pts, int)

                assert isinstance(description, str)

    def test_no_duplicate_book_names(self):

        """Nie ma duplikatów nazw książek"""

        books = load_books_from_json(JSON_PATH)

        names = [b["name"] for b in books]

        assert len(names) == len(set(names)), "Duplicate book names found"

    def test_points_are_non_negative(self):

        """Wszystkie punkty są nieujemne"""

        books = load_books_from_json(JSON_PATH)

        for book in books:

            for rule in book["rules"]:

                assert rule[1] >= 0, f"Negative points in {book['name']}"

    def test_total_points_sum_to_100(self):

        """Każda książka ma łącznie 100 punktów"""

        books = load_books_from_json(JSON_PATH)

        for book in books:

            total_points = sum(rule[1] for rule in book["rules"])

            assert total_points == 100, f"Book '{book['name']}' total {total_points} != 100"
