from app import (
    sugerowany_gatunek_dla_godziny,
    sugerowany_klimat_dla_nastroju,
    szacowany_czas_czytania,
    sugerowane_tempo_dla_czasu_wolnego,
    sugerowany_swiat_dla_pory_roku
)


def test_genre_for_time():
    assert sugerowany_gatunek_dla_godziny() in [
        "biografia", "reportaz", "thriller", "romans", "horror"
    ]


def test_climate_for_mood_mapping():
    assert sugerowany_klimat_dla_nastroju("dobry") == "przygodowy"
    assert sugerowany_klimat_dla_nastroju("zly") == "mroczny"


def test_reading_time_minimum():
    assert szacowany_czas_czytania("krotka") == 180


def test_reading_time_fast():
    assert szacowany_czas_czytania("srednia", tempo_czytania="szybkie") == 336


def test_suggested_tempo():
    assert sugerowane_tempo_dla_czasu_wolnego(30) == "dynamiczne"
    assert sugerowane_tempo_dla_czasu_wolnego(200) == "powolne"


def test_suggested_world():
    assert sugerowany_swiat_dla_pory_roku() in [
        "przyszlosc", "wspolczesny", "magiczny", "historyczny"
    ]
