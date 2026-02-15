import itertools

from KSIAZKI_razem import wybierz_ksiazke


def test_all_possible_combinations_do_not_crash():
    """
    Test eksploracyjny:
    - sprawdza czy silnik działa dla wielu kombinacji
    - nie sprawdza 'jakości' rekomendacji
    - wykrywa błędy Context, resolvera, reguł i JSON
    """

    gatunek = ["fantasy", "kryminal", "romans"]
    klimat = ["mroczny", "lekki", "realistyczny"]
    tempo = ["wolne", "umiarkowane", "dynamiczne"]
    dlugosc = ["krotka", "srednia"]

    combinations = list(itertools.product(
        gatunek, klimat, tempo, dlugosc
    ))

    assert len(combinations) == 54  # sanity check

    for combo in combinations:
        profil = {
            "gatunek": combo[0],
            "klimat": combo[1],
            "tempo": combo[2],
            "dlugosc": combo[3]
        }

        wynik = wybierz_ksiazke(profil)

        # --- ASSERTY SYSTEMOWE ---
        assert "top3" in wynik
        assert len(wynik["top3"]) == 3
        assert all("name" in b for b in wynik["top3"])
        assert all("score" in b for b in wynik["top3"])

        # punkty nie mogą być ujemne
        assert all(b["score"] >= 0 for b in wynik["top3"])