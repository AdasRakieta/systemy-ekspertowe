from app import (
    szacowany_czas_czytania,
    sugerowane_tempo_dla_czasu_wolnego,
    sugerowany_gatunek_dla_godziny,
    sugerowany_swiat_dla_pory_roku
)


class TestBusinessLogicAccuracy:

    """Testy dokładności obliczeń biznesowych dla książek"""

    def test_reading_time_base_short(self):

        """Bazowy czas dla krótkiej książki"""

        assert szacowany_czas_czytania("krotka") == 180

    def test_reading_time_base_long(self):

        """Bazowy czas dla długiej książki"""

        assert szacowany_czas_czytania("dluga") == 900

    def test_reading_time_slow_multiplier(self):

        """Wolne tempo wydłuża czas"""

        assert szacowany_czas_czytania("srednia", tempo_czytania="wolne") == 720

    def test_reading_time_fast_multiplier(self):

        """Szybkie tempo skraca czas"""

        assert szacowany_czas_czytania("srednia", tempo_czytania="szybkie") == 336

    def test_tempo_suggestion_thresholds(self):

        """Sugestia tempa zależy od czasu wolnego"""

        assert sugerowane_tempo_dla_czasu_wolnego(45) == "dynamiczne"
        assert sugerowane_tempo_dla_czasu_wolnego(120) == "umiarkowane"
        assert sugerowane_tempo_dla_czasu_wolnego(240) == "powolne"

    def test_context_suggestions_ranges(self):

        """Sugestie kontekstowe zwracają poprawne wartości"""

        assert sugerowany_gatunek_dla_godziny() in [
            "biografia", "reportaz", "thriller", "romans", "horror"
        ]
        assert sugerowany_swiat_dla_pory_roku() in [
            "przyszlosc", "wspolczesny", "magiczny", "historyczny"
        ]
