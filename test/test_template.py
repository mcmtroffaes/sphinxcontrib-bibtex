from sphinxcontrib.bibtex.style.referencing import join, sentence


def test_join() -> None:
    assert str(join.format()) == ""
    assert str(join['a', 'b', 'c', 'd', 'e'].format()) == "abcde"
    join_sep = join(sep=', ', sep2=' and ', last_sep=', and ')
    assert str(join_sep['Tom', 'Jerry'].format()) == "Tom and Jerry"
    assert str(join_sep['Billy', 'Willy', 'Dilly'].format()) \
           == "Billy, Willy, and Dilly"
    join_other = join(other=' et al.')
    assert str(join_other['Billy', 'Willy', 'Dilly'].format()) \
           == "Billy et al."


def test_sentence() -> None:
    assert str(sentence.format()) == ""
    assert \
        str(sentence(capitalize=True, sep=' ')[
            'mary', 'had', 'a', 'little', 'lamb'].format()) == \
        "Mary had a little lamb."
    assert \
        str(sentence(capitalize=False, add_period=False)[
                'uno', 'dos', 'tres'].format()) == \
        "uno, dos, tres"
    assert str(sentence(capfirst=True, other=' and more')[
                   'uno', 'dos', 'tres'].format()) == \
        "Uno and more."
