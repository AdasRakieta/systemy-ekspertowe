from Kawa_silnik import wybierz_kawe

def test_top3_length():
    profil = {
        "moc": "wysoka",
        "mleko": "brak",
        "slodycz": "niska",
        "wielkosc": "mala",
        "temperatura": "gorąca",
        "kofeina": "wysoka"
    }
    wynik = wybierz_kawe(profil)
    assert len(wynik["top3"]) == 3

def test_scores_sorted_desc():
    profil = {
        "moc": "średnia",
        "mleko": "średnio",
        "slodycz": "niska",
        "wielkosc": "srednia",
        "temperatura": "gorąca",
        "kofeina": "średnia"
    }
    scores = [c["score"] for c in wybierz_kawe(profil)["top3"]]
    assert scores == sorted(scores, reverse=True)

def test_scores_non_negative():
    profil = {
        "moc": "niska",
        "mleko": "dużo",
        "slodycz": "wysoka",
        "wielkosc": "duza",
        "temperatura": "zimna",
        "kofeina": "niska"
    }
    for c in wybierz_kawe(profil)["top3"]:
        assert c["score"] >= 0
