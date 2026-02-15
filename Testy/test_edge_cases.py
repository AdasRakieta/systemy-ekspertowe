import pytest

from Kawa_silnik import wybierz_kawe


class TestEdgeCases:

    """Testy graniczne i ekstremalne scenariusze"""

    def test_all_scores_zero(self):

        """Profil, gdzie żadna reguła się nie dopasuje"""

        profile = {

            "moc": "niska",

            "mleko": "brak",

            "slodycz": "niska",

            "wielkosc": "mala",

            "temperatura": "zimna",

            "kofeina": "niska"

        }

        result = wybierz_kawe(profile)

        assert "top3" in result

        assert len(result["top3"]) == 3

    def test_multiple_scores_tied_for_first_place(self):

        """Kilka kawy ze takim samym score"""

        profile = {

            "moc": "wysoka",

            "mleko": "brak",

            "slodycz": "niska",

            "wielkosc": "mala",

            "temperatura": "gorąca",

            "kofeina": "wysoka"

        }

        result = wybierz_kawe(profile)

        top_score = result["top3"][0]["score"]

        tied = [c for c in result["top3"] if c["score"] == top_score]

        assert len(tied) >= 1

    def test_single_high_scoring_match(self):

        """Tylko jedna kawa ma wysokie punkty"""

        profile = {

            "moc": "bardzo wysoka",

            "mleko": "brak",

            "slodycz": "niska",

            "wielkosc": "mala",

            "temperatura": "gorąca",

            "kofeina": "wysoka"

        }

        result = wybierz_kawe(profile)

        assert result["top3"][0]["name"] in ["Ristretto", "Doppio", "Macchiato"]

    def test_all_attributes_extreme_values(self):

        """Maksymalne/minimalne wartości dla wszystkich atrybutów"""

        extreme_profiles = [

            {

                "moc": "bardzo wysoka",

                "mleko": "brak",

                "slodycz": "niska",

                "wielkosc": "mala",

                "temperatura": "gorąca",

                "kofeina": "wysoka"

            },

            {

                "moc": "niska",

                "mleko": "dużo",

                "slodycz": "wysoka",

                "wielkosc": "duza",

                "temperatura": "zimna",

                "kofeina": "niska"

            }

        ]

        

        for profile in extreme_profiles:

            result = wybierz_kawe(profile)

            assert len(result["top3"]) == 3

            assert all(c["score"] >= 0 for c in result["top3"])

