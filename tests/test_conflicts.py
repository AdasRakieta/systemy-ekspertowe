from app import wybierz_ksiazke


def test_conflicting_rules_multiple_winners():
    profil = {
        "gatunek": "reportaz",
        "klimat": "realistyczny",
        "miejsce": "miasto",
        "dlugosc": "srednia",
        "tempo": "dynamiczne"
    }

    wynik = wybierz_ksiazke(profil)
    top3 = wynik["top3"]

    max_score = top3[0]["score"]
    winners = [b for b in top3 if b["score"] == max_score]

    # Konflikt = więcej niż jeden zwycięzca
    assert len(winners) >= 2
