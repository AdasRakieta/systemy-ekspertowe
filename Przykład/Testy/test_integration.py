from KSIAZKI_razem import wybierz_ksiazke


def test_full_flow():
    profil = {
        "gatunek": "thriller",
        "klimat": "psychologiczny",
        "tempo": "dynamiczne",
        "dlugosc": "srednia",
        "wiek_bohatera": "dorosly"
    }

    wynik = wybierz_ksiazke(profil)

    assert "top3" in wynik
    assert "wyjasnienia" in wynik
    assert len(wynik["top3"]) == 3
    assert wynik["top3"][0]["score"] > 0

