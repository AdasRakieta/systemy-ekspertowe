import pytest
import rule_engine

def test_rule_positive_match():
    rule = rule_engine.Rule("gatunek == 'fantasy' and klimat == 'mroczny'")
    data = {"gatunek": "fantasy", "klimat": "mroczny"}
    assert rule.matches(data)

def test_rule_negative_match():
    rule = rule_engine.Rule("gatunek == 'fantasy' and klimat == 'mroczny'")
    data = {"gatunek": "romans", "klimat": "mroczny"}
    assert not rule.matches(data)

def test_rule_in_operator():
    rule = rule_engine.Rule("gatunek in ['fantasy', 'romans']")
    assert rule.matches({"gatunek": "fantasy"})
    assert rule.matches({"gatunek": "romans"})
    assert not rule.matches({"gatunek": "kryminal"})

def test_rule_not_equal():
    rule = rule_engine.Rule("tempo != 'wolne'")
    assert rule.matches({"tempo": "dynamiczne"})
    assert not rule.matches({"tempo": "wolne"})

def test_rule_missing_field():
    rule = rule_engine.Rule("klimat == 'mroczny'")
    with pytest.raises(rule_engine.errors.SymbolResolutionError):
        rule.matches({"gatunek": "fantasy"})
