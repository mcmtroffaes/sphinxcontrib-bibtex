from pybtex.database import Person, Entry
from pybtex.plugin import find_plugin
from pybtex.richtext import HRef
from pybtex.style.formatting import BaseStyle
from pybtex.style.template import Node, FieldIsMissing
from sphinxcontrib.bibtex.style.referencing import (
    BaseReferenceText, BaseReferenceStyle,
    entry_label, reference, join, names
)
from typing import TYPE_CHECKING, List, cast
import pytest

if TYPE_CHECKING:
    from pybtex.richtext import BaseText


def test_style_names_last():
    from pybtex.database import Person
    from sphinxcontrib.bibtex.style.names.last import NameStyle
    name = Person(
        string=r"Charles Louis Xavier Joseph de la Vall{\'e}e Poussin")
    last = NameStyle().format
    assert last(name).format().render_as('latex') == "de~la Vall{é}e~Poussin"
    assert (
        last(name).format().render_as('html') ==
        'de&nbsp;la Vall<span class="bibtex-protected">é</span>e&nbsp;Poussin')
    name2 = Person(first='First', last='Last', middle='Middle')
    assert last(name2).format().render_as('latex') == "Last"


def test_style_names_no_author():
    entry = Entry(type_='book')
    with pytest.raises(FieldIsMissing):
        names('author').format_data(dict(entry=entry))


class SimpleReferenceStyle(BaseReferenceStyle):

    def get_role_names(self):
        return 'p'

    def get_outer_template(
            self, role_name: str, children: List["BaseText"]) -> "Node":
        return join['{', join(';')[children], '}']

    def get_inner_template(self, role_name: str) -> "Node":
        return reference[entry_label]


class SimpleReferenceText(BaseReferenceText[str]):
    """A simple reference text class storing the url as a string in *info*."""

    def render(self, backend):
        url = self.info[0]
        return HRef(url, *self.parts).render(backend)


def test_simple_reference_style():
    cit_style = cast(
        BaseStyle, find_plugin('pybtex.style.formatting', 'unsrtalpha')())
    ref_style = SimpleReferenceStyle(SimpleReferenceText)
    auth1 = Person('First Last')
    auth2 = Person('Ein Zwei')
    auth3 = Person('Primo Secundo')
    fields1 = dict(title='The Book', year='2000', publisher='Santa')
    entry1 = Entry(type_='book', fields=fields1, persons=dict(author=[auth1]))
    entry2 = Entry(type_='book', fields=fields1, persons=dict(author=[auth2]))
    entry3 = Entry(type_='book', fields=fields1, persons=dict(author=[auth3]))
    entries = [entry1, entry2, entry3]
    formatted_entries = list(cit_style.format_entries(entries))
    infos = ["#id1", "#id2", "#id3"]
    references = list(zip(entries, formatted_entries, infos))
    backend = find_plugin('pybtex.backends', 'html')()
    assert \
        ref_style.format_references('p', references).render(backend) == \
        '{<a href="#id1">Las00</a>;<a href="#id2">Zwe00</a>' \
        ';<a href="#id3">Sec00</a>}'
