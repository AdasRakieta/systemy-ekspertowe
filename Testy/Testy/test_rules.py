import rule_engine

def test_rule_positive_match():
    rule = rule_engine.Rule("moc == 'wysoka' and mleko == 'brak'")
    data = {"moc": "wysoka", "mleko": "brak"}
    assert rule.matches(data)

def test_rule_negative_match():
    rule = rule_engine.Rule("moc == 'wysoka' and mleko == 'brak'")
    data = {"moc": "niska", "mleko": "brak"}
    assert not rule.matches(data)

def test_rule_in_operator():
    rule = rule_engine.Rule("moc in ['średnia', 'wysoka']")
    assert rule.matches({"moc": "wysoka"})
    assert rule.matches({"moc": "średnia"})
    assert not rule.matches({"moc": "niska"})

def test_rule_not_equal():
    rule = rule_engine.Rule("mleko != 'brak'")
    assert rule.matches({"mleko": "dużo"})
    assert not rule.matches({"mleko": "brak"})

def test_rule_missing_field():
    rule = rule_engine.Rule("slodycz == 'wysoka'")
    assert not rule.matches({"moc": "wysoka"})
