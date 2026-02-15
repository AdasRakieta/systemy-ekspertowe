from KSIAZKI_razem import wybierz_ksiazke


class TestEdgeCases:

    """Testy graniczne i ekstremalne scenariusze"""

    def test_all_scores_zero(self):

        """Profil, gdzie żadna reguła się nie dopasuje"""

        profile = {

            "gatunek": "nieznany_gatunek",

            "klimat": "nieznany_klimat",

            "dlugosc": "nieznana",

            "tempo": "nieznane",

            "wiek_bohatera": "nieznany"

        }

        result = wybierz_ksiazke(profile)

        assert "top3" in result

        assert len(result["top3"]) == 3

        assert all(b["score"] == 0 for b in result["top3"])

    def test_multiple_scores_tied_for_first_place(self):

        """Kilka książek z takim samym wynikiem"""

        profile = {

            "gatunek": "reportaz",

            "klimat": "realistyczny",

            "miejsce": "miasto",

            "dlugosc": "srednia",

            "tempo": "dynamiczne"

        }

        result = wybierz_ksiazke(profile)

        top_score = result["top3"][0]["score"]

        tied = [b for b in result["top3"] if b["score"] == top_score]

        assert len(tied) >= 2

    def test_single_high_scoring_match(self):

        """Jedna książka powinna zdecydowanie wygrać"""

        profile = {

            "gatunek": "fantasy",

            "dlugosc": "bardzo_dluga",

            "tempo": "dynamiczne",

            "wiek_bohatera": "mlody",

            "swiat": "magiczny"

        }

        result = wybierz_ksiazke(profile)

        assert result["top3"][0]["name"] == "Władca Pierścieni - J.R.R. Tolkien"

        assert result["top3"][0]["score"] == 100

    def test_all_attributes_extreme_values(self):

        """Maksymalne/minimalne wartości dla wszystkich atrybutów"""

        extreme_profiles = [

            {

                "gatunek": "horror",

                "klimat": "gotycki",

                "dlugosc": "krotka",

                "tempo": "wolne",

                "miejsce": "zamek"

            },

            {

                "gatunek": "poezja",

                "klimat": "liryczny",

                "dlugosc": "krotka",

                "tempo": "wolne",

                "wiek_bohatera": "brak"

            }

        ]

        

        for profile in extreme_profiles:

            result = wybierz_ksiazke(profile)

            assert len(result["top3"]) == 3

            assert all(b["score"] >= 0 for b in result["top3"])

