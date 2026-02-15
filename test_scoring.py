from app import wybierz_ksiazke


def test_top3_length():
    profil = {
        "gatunek": "thriller",
        "klimat": "psychologiczny",
        "tempo": "dynamiczne",
        "dlugosc": "srednia"
    }
    wynik = wybierz_ksiazke(profil)
    assert len(wynik["top3"]) == 3


def test_scores_sorted_desc():
    profil = {
        "gatunek": "kryminal",
        "klimat": "mroczny",
        "tempo": "wolne",
        "dlugosc": "dluga"
    }
    scores = [b["score"] for b in wybierz_ksiazke(profil)["top3"]]
    assert scores == sorted(scores, reverse=True)


def test_scores_non_negative():
    profil = {
        "gatunek": "romans",
        "klimat": "lekki",
        "tempo": "umiarkowane",
        "dlugosc": "srednia"
    }
    for b in wybierz_ksiazke(profil)["top3"]:
        assert b["score"] >= 0
