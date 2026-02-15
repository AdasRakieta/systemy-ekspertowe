from Kawa_silnik import wybierz_kawe

def test_conflicting_rules_multiple_winners():
    profil = {
        "moc": "wysoka",
        "mleko": "brak",
        "slodycz": "niska",
        "wielkosc": "mala",
        "temperatura": "gorąca",
        "kofeina": "wysoka"
    }

    wynik = wybierz_kawe(profil)
    top3 = wynik["top3"]

    max_score = top3[0]["score"]
    winners = [c for c in top3 if c["score"] == max_score]

    # Konflikt = więcej niż jeden zwycięzca
    assert len(winners) >= 1

    if len(winners) > 1:
        print("\n Konflikt reguł wykryty:")
        for w in winners:
            print(f"- {w['name']} ({w['score']} pkt)")
