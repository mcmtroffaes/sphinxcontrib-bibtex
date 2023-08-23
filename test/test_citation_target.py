import pytest

from sphinxcontrib.bibtex.citation_target import parse_citation_targets


@pytest.mark.parametrize(
    "target,expected",
    [
        ("abc", [("abc", "", "")]),
        ("{xyz}abc", [("abc", "xyz", "")]),
        ("abc{xyz}", [("abc", "", "xyz")]),
        ("{xyz}abc{123}", [("abc", "xyz", "123")]),
        ("  {xyz} abc  {123}   ", [("abc", "xyz", "123")]),
        ("abc,def", [("abc", "", ""), ("def", "", "")]),
        ("  abc ,   def  ", [("abc", "", ""), ("def", "", "")]),
        (
            "  {xyz }abc  {123} ,  {hi hi} def {oops, blah } ",
            [("abc", "xyz ", "123"), ("def", "hi hi", "oops, blah ")],
        ),
    ],
)
def test_citation_target(target, expected) -> None:
    assert list(parse_citation_targets(target)) == expected


@pytest.mark.parametrize(
    "target",
    [
        "}",
        "{}}",
        "abc}",
        "abc{}}",
        "",
        ",",
        ",a",
        "a,",
        "{}a",
        "a{}",
        "{a}b{}",
        "{}a{b}",
    ],
)
def test_citation_target_invalid(target) -> None:
    with pytest.raises(ValueError, match="malformed citation target"):
        list(parse_citation_targets(target))
