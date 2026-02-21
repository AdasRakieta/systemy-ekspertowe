from app import wybierz_ksiazke


def test_fantasy_still_top():
    profil = {
        "gatunek": "fantasy",
        "dlugosc": "bardzo_dluga",
        "tempo": "dynamiczne",
        "wiek_bohatera": "mlody",
        "swiat": "magiczny"
    }

    names = [b["name"] for b in wybierz_ksiazke(profil)["top3"]]
    assert "Władca Pierścieni - J.R.R. Tolkien" in names


def test_dracula_for_gothic_profile():
    profil = {
        "gatunek": "horror",
        "klimat": "gotycki",
        "miejsce": "zamek",
        "dlugosc": "krotka",
        "tempo": "wolne"
    }

    names = [b["name"] for b in wybierz_ksiazke(profil)["top3"]]
    assert "Dracula - Bram Stoker" in names

