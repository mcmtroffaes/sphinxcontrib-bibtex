import pybtex.plugin

from pybtex.database import Person, Entry
from pybtex.richtext import HRef
from pybtex.style.template import Node, FieldIsMissing
# direct import of the plugin to ensure we are testing this specific class
from sphinxcontrib.bibtex.style.names.last import LastNameStyle
from sphinxcontrib.bibtex.style.referencing import (
    BaseReferenceText, BaseReferenceStyle, format_references
)
from sphinxcontrib.bibtex.style.referencing.basic_author_year import (
    BasicAuthorYearTextualReferenceStyle
)
from sphinxcontrib.bibtex.style.template import (
    entry_label, reference, join, names
)
from typing import TYPE_CHECKING, List, Iterable
import pytest

if TYPE_CHECKING:
    from pybtex.backends import BaseBackend
    from pybtex.richtext import BaseText
    from pybtex.style.formatting import BaseStyle


def test_style_names_last() -> None:
    name = Person(
        string=r"Charles Louis Xavier Joseph de la Vall{\'e}e Poussin")
    last = LastNameStyle().format
    assert last(name).format().render_as('latex') == "de~la Vall{é}e~Poussin"
    assert (
        last(name).format().render_as('html') ==
        'de&nbsp;la Vall<span class="bibtex-protected">é</span>e&nbsp;Poussin')
    name2 = Person(first='First', last='Last', middle='Middle')
    assert last(name2).format().render_as('latex') == "Last"


def test_style_names() -> None:
    auth = Person('First Last')
    fields = dict(title='The Book', year='2000', publisher='Santa')
    entry = Entry(type_='book', fields=fields, persons=dict(author=[auth]))
    style = BasicAuthorYearTextualReferenceStyle()
    rich_name = style.person.names('author', full=True).format_data(
        dict(entry=entry, style=style))
    assert rich_name.render_as('text') == "Last"


def test_style_names_no_author() -> None:
    entry = Entry(type_='book')
    with pytest.raises(FieldIsMissing):
        names('author').format_data(dict(entry=entry))


class SimpleReferenceStyle(BaseReferenceStyle):

    def role_names(self) -> Iterable[str]:
        return ['p']

    def outer(self, role_name: str, children: List["BaseText"]) -> "Node":
        return join['{', join(';')[children], '}']

    def inner(self, role_name: str) -> "Node":
        return reference[entry_label]


class SimpleReferenceText(BaseReferenceText[str]):
    """A simple reference text class storing the url as a string in *info*."""

    def render(self, backend):
        url = self.info[0]
        return HRef(url, *self.parts).render(backend)


def test_simple_reference_style() -> None:
    cit_style: "BaseStyle" = \
        pybtex.plugin.find_plugin('pybtex.style.formatting', 'unsrtalpha')()
    ref_style = SimpleReferenceStyle()
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
    backend: "BaseBackend" = \
        pybtex.plugin.find_plugin('pybtex.backends', 'html')()
    assert 'p' in ref_style.role_names()
    assert \
        format_references(ref_style, SimpleReferenceText,
                          'p', references).render(backend) == \
        '{<a href="#id1">Las00</a>;<a href="#id2">Zwe00</a>' \
        ';<a href="#id3">Sec00</a>}'
