from Kawa_silnik import wybierz_kawe

def test_espresso_still_top():
    profil = {
        "moc": "wysoka",
        "mleko": "brak",
        "slodycz": "niska",
        "wielkosc": "mala",
        "temperatura": "gorąca",
        "kofeina": "wysoka"
    }

    names = [c["name"] for c in wybierz_kawe(profil)["top3"]]
    assert "Espresso" in names

def test_cold_brew_for_cold_profile():
    profil = {
        "moc": "wysoka",
        "mleko": "brak",
        "slodycz": "niska",
        "wielkosc": "duza",
        "temperatura": "zimna",
        "kofeina": "wysoka"
    }

    names = [c["name"] for c in wybierz_kawe(profil)["top3"]]
    assert "Cold Brew" in names

