import pytest

from Kawa_silnik import oblicz_koszt_kawy, czas_przygotowania


class TestBusinessLogicAccuracy:

    """Testy dokładności obliczeń biznesowych"""

    def test_cost_calculation_exact(self):

        """Dokładne obliczenie ceny"""

        cost = oblicz_koszt_kawy(10.0, mleko_ml=100, syrop_ml=20, 

                                  dodatki=["kakao", "cynamon"])

        assert cost == pytest.approx(14.50, rel=0.01)

    def test_cost_with_unknown_addon_ignored(self):

        """Nieznany dodatek powinien być zignorowany"""

        cost = oblicz_koszt_kawy(10.0, dodatki=["nieznany_dodatek"])

        assert cost == 10.0

    def test_cost_rounding_to_2_decimals(self):

        """Wynik powinien być zaokrąglony do 2 miejsc"""

        cost = oblicz_koszt_kawy(10.0, mleko_ml=33, syrop_ml=17)

        assert cost == pytest.approx(11.51, rel=0.01)

        assert len(str(cost).split('.')[-1]) <= 2

    def test_time_preparation_espresso_base(self):

        """Czas bazowy dla espresso"""

        time = czas_przygotowania("espresso")

        assert time == 25

    def test_time_preparation_with_multiple_shots(self):

        """Czas dla multiple shotów"""

        time_2_shots = czas_przygotowania("espresso", liczba_shotów=2)

        assert time_2_shots == 45

    def test_time_preparation_with_milk_steaming(self):

        """Czas z parą mleka"""

        time_with_milk = czas_przygotowania("espresso", spienianie_mleka=True)

        assert time_with_milk == 55

    def test_time_preparation_combined(self):

        """Czas łączony: 2 shotów + parowanie mleka"""

        time = czas_przygotowania("espresso", liczba_shotów=2, spienianie_mleka=True)

        assert time == 75

    def test_time_cold_brew_very_long(self):

        """Cold Brew wymaga 4 godzin"""

        time = czas_przygotowania("cold_brew")

        assert time == 4 * 3600
