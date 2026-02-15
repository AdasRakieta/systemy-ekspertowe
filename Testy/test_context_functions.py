from Kawa_silnik import (
    sugerowana_kofeina_dla_godziny,
    oblicz_koszt_kawy,
    czas_przygotowania,
    sugerowana_moc_dla_wrazliwosci,
    sugerowana_kofeina_dla_wrazliwosci
)

def test_kofeina_for_time():
    assert sugerowana_kofeina_dla_godziny() in [
        "wysoka", "średnia", "niska", "bardzo_niska"
    ]

def test_cost_minimum():
    assert oblicz_koszt_kawy(8.0) == 8.0

def test_cost_with_addons():
    cost = oblicz_koszt_kawy(
        8.0, mleko_ml=100, syrop_ml=20, dodatki=["kakao", "cynamon"]
    )
    assert cost > 10.0

def test_time_with_two_shots_and_milk():
    t = czas_przygotowania("espresso", liczba_shotów=2, spienianie_mleka=True)
    assert t >= 75

def test_suggested_strength():
    assert sugerowana_moc_dla_wrazliwosci("wysoka") == "niska"
    assert sugerowana_moc_dla_wrazliwosci("niska") == "wysoka"

def test_suggested_caffeine():
    assert sugerowana_kofeina_dla_wrazliwosci("wysoka") == "niska"
    assert sugerowana_kofeina_dla_wrazliwosci("niska") == "wysoka"
