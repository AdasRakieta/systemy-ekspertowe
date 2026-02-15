from Kawa_silnik import wybierz_kawe

def test_full_flow():
    profil = {
        "moc": "bardzo wysoka",
        "mleko": "brak",
        "slodycz": "niska",
        "wielkosc": "mala",
        "temperatura": "gorąca",
        "kofeina": "wysoka"
    }

    wynik = wybierz_kawe(profil)

    assert "top3" in wynik
    assert "wyjasnienia" in wynik
    assert len(wynik["top3"]) == 3
    assert wynik["top3"][0]["score"] > 0

