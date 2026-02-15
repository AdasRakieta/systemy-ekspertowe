import itertools
from Kawa_silnik import wybierz_kawe

def test_all_possible_combinations_do_not_crash():
    """
    Test eksploracyjny:
    - sprawdza czy silnik działa dla KAŻDEJ kombinacji
    - nie sprawdza 'jakości' rekomendacji
    - wykrywa błędy Context, resolvera, reguł i JSON
    """

    moc = ["niska", "średnia", "wysoka", "bardzo wysoka"]
    mleko = ["brak", "mało", "średnio", "dużo"]
    slodycz = ["niska", "średnia", "wysoka"]
    wielkosc = ["mala", "srednia", "duza"]
    temperatura = ["gorąca", "zimna"]
    kofeina = ["niska", "średnia", "wysoka"]

    combinations = list(itertools.product(
        moc, mleko, slodycz, wielkosc, temperatura, kofeina
    ))

    assert len(combinations) == 864  # sanity check

    for combo in combinations:
        profil = {
            "moc": combo[0],
            "mleko": combo[1],
            "slodycz": combo[2],
            "wielkosc": combo[3],
            "temperatura": combo[4],
            "kofeina": combo[5]
        }

        wynik = wybierz_kawe(profil)

        # --- ASSERTY SYSTEMOWE ---
        assert "top3" in wynik
        assert len(wynik["top3"]) == 3
        assert all("name" in c for c in wynik["top3"])
        assert all("score" in c for c in wynik["top3"])

        # punkty nie mogą być ujemne
        assert all(c["score"] >= 0 for c in wynik["top3"])

test_all_possible_combinations_do_not_crash()