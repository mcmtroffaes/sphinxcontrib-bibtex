import dataclasses

from enum import Enum

from pybtex.plugin import Plugin
from pybtex.richtext import Text, BaseMultipartText, Tag
from pybtex.style.template import node, _format_list, FieldIsMissing, field
from typing import (
    TYPE_CHECKING, TypeVar, Generic, Tuple, List, Union, NamedTuple, Iterator
)
from typing import Iterable, Optional, cast, Any, Type, Dict

from sphinxcontrib.bibtex.style.names.last import NameStyle as LastNameStyle

if TYPE_CHECKING:
    from pybtex.database import Entry
    from pybtex.richtext import BaseText
    from pybtex.style import FormattedEntry
    from pybtex.style.names import BaseNameStyle
    from pybtex.style.template import Node


ReferenceInfo = TypeVar('ReferenceInfo')
"""Generic type parameter for types that store reference information.
To be implemented by clients; see for instance :class:`SphinxReferenceInfo`.
"""


# copied from pybtex join but extended to allow "et al" formatting
@node
def join(children, data, sep='', sep2=None, last_sep=None, other=None):
    """Join text fragments together."""

    if sep2 is None:
        sep2 = sep
    if last_sep is None:
        last_sep = sep
    parts = [part for part in _format_list(children, data) if part]
    if len(parts) <= 1:
        return Text(*parts)
    elif len(parts) == 2:
        return Text(sep2).join(parts)
    elif other is None:
        return Text(last_sep).join([Text(sep).join(parts[:-1]), parts[-1]])
    else:
        return Text(parts[0], other)


# copied from pybtex names but using the new join
@node
def sentence(children, data, capfirst=False, capitalize=False, add_period=True,
             sep=', ', sep2=None, last_sep=None, other=None):
    """Join text fragments, capitalize the first letter,
    and add a period to the end.
    """
    text = join(sep=sep, sep2=sep2, last_sep=last_sep, other=other)[
        children
    ].format_data(data)
    if capfirst:
        text = text.capfirst()
    if capitalize:
        text = text.capitalize()
    if add_period:
        text = text.add_period()
    return text


# copied from pybtex names but using the new join allowing "et al" formatting
@node
def names(children, data, role, **kwargs):
    """Return formatted names."""
    assert not children
    try:
        persons = data['entry'].persons[role]
    except KeyError:
        raise FieldIsMissing(role, data['entry'])
    style = data['style']
    formatted_names = [style.name_style.format(person, style.abbreviate_names)
                       for person in persons]
    return join(**kwargs)[formatted_names].format_data(data)


@node
def entry_label(children, data) -> "BaseText":
    """Node for inserting the label of a formatted entry."""
    assert not children
    entry = cast("FormattedEntry", data['formatted_entry'])
    return Text(entry.label)


@node
def reference(children, data: Dict[str, Any]):
    """Node for inserting a citation reference. The children of the node
    comprise the content of the reference, and any referencing information
    is stored in the *reference_info* key of the *data*.
    The data must also contain a *style* key pointing to the
    corresponding :class:`BaseReferenceStyle`.
    """
    parts = _format_list(children, data)
    style = cast(BaseReferenceStyle, data['style'])
    info = data['reference_info']
    return style.ReferenceText(info, *parts)


class BaseReferenceText(BaseMultipartText, Generic[ReferenceInfo]):
    """Generic rich text element for citation references.
    Instances store some extra reference info that can be used when formatting.
    This base class renders its children without further formatting.
    Implementations must create a derivation from this class which
    overrides the *render* method to create the desired output.
    See for instance :class:`SphinxReferenceText`.
    """

    def __init__(self, info: ReferenceInfo, *parts: "BaseText"):
        self.info = (info,)
        super().__init__(*parts)


class RoleType(Enum):
    """Different citation types."""
    PARENTHETICAL = 'p'
    TEXTUAL = 't'
    LABEL = 'label'
    YEAR = 'year'
    AUTHOR = 'author'


class Role(NamedTuple):
    """Stores the type and features of a citation reference role."""
    type_: RoleType
    capfirst: bool
    brackets: bool
    full_authors: bool

    def name(self):
        cap = 'cap' if self.capfirst else ''
        if self.type_ in {RoleType.PARENTHETICAL, RoleType.TEXTUAL}:
            bra = '' if self.brackets else 'al'
            par = ''
        else:
            bra = ''
            par = 'par' if self.brackets else ''
        ful = 's' if self.full_authors else ''
        return f'{cap}{bra}{self.type_.value}{par}{ful}'


class Separators(NamedTuple):
    sep: Union["BaseText", str] = ''
    sep2: Optional[Union["BaseText", str]] = None
    last_sep: Optional[Union["BaseText", str]] = None
    other: Optional[Union["BaseText", str]] = None


# can get rid of this in Python 3.8+ with an assignment expression
_roles = [
    Role(
        type_=type_,
        capfirst=capfirst,
        brackets=brackets,
        full_authors=full_authors,
    )
    for type_ in RoleType
    for brackets in (False, True)
    for capfirst in (
        (False, True) if RoleType not in (RoleType.LABEL, RoleType.YEAR)
        else (False,))
    for full_authors in (
        (False, True) if RoleType not in (RoleType.LABEL, RoleType.YEAR)
        else (False,))
]

roles_by_name: Dict[str, Role] = {role.name(): role for role in _roles}
"""Convenience dictionary mapping each role name to a :class:`Role`."""


@dataclasses.dataclass(eq=False)
class BaseReferenceStyle(Plugin, Generic[ReferenceInfo]):
    """Base class for reference styles.
    Custom styles can override the outer and inner templates.
    """

    ReferenceText: Type[BaseReferenceText[ReferenceInfo]]
    name_style: "BaseNameStyle" = dataclasses.field(
        default_factory=lambda: LastNameStyle())
    abbreviate_names: bool = True
    left_bracket: Union["BaseText", str] = '['
    right_bracket: Union["BaseText", str] = ']'
    outer_separators: Dict[RoleType, Separators] = dataclasses.field(
        default_factory=lambda: {
            role_type: Separators(sep=', ') for role_type in RoleType
        }
    )
    names_separators: Separators = dataclasses.field(
        default_factory=lambda: Separators(
            sep=', ', sep2=' and ', last_sep=', and ',
            other=Text(' ', Tag('em', 'et al.')))
    )

    def _data_from_references(
            self,
            references: Iterable[Tuple[
                "Entry", "FormattedEntry", ReferenceInfo]]
            ) -> Iterator[Dict[str, Any]]:
        for entry, formatted_entry, info in references:
            yield dict(entry=entry, formatted_entry=formatted_entry,
                       style=self, reference_info=info)

    def format_references(
            self, role: Role,
            references: Iterable[Tuple[
                "Entry", "FormattedEntry", ReferenceInfo]],
            ) -> "BaseText":
        children = [
            self.get_inner_template(role).format_data(data)
            for data in self._data_from_references(references)]
        return self.get_outer_template(role, children).format()

    def get_outer_template(
            self, role: Role, children: List["BaseText"]) -> "Node":
        func_name = "get_{}_outer_template".format(role.type_.name.lower())
        return getattr(self, func_name)(role, children)

    def get_inner_template(self, role: Role) -> "Node":
        func_name = "get_{}_inner_template".format(role.type_.name.lower())
        return getattr(self, func_name)(role)

    def get_parenthetical_outer_template(
            self, role: Role, children: List["BaseText"]) -> "Node":
        raise NotImplementedError

    def get_parenthetical_inner_template(self, role: Role) -> "Node":
        raise NotImplementedError

    def get_textual_outer_template(
            self, role: Role, children: List["BaseText"]) -> "Node":
        raise NotImplementedError

    def get_textual_inner_template(self, role: Role) -> "Node":
        raise NotImplementedError

    def get_label_outer_template(
            self, role: Role, children: List["BaseText"]) -> "Node":
        return self.get_outer_template_helper(
            children,
            separators=self.outer_separators[role.type_],
            brackets=role.brackets,
            capfirst=False,
        )

    def get_label_inner_template(self, role: Role) -> "Node":
        return reference[entry_label]

    def get_year_outer_template(
            self, role: Role, children: List["BaseText"]) -> "Node":
        return self.get_outer_template_helper(
            children,
            separators=self.outer_separators[role.type_],
            brackets=role.brackets,
            capfirst=False,
        )

    def get_year_inner_template(self, role: Role) -> "Node":
        return reference[field('year')]

    def get_author_outer_template(
            self, role: Role, children: List["BaseText"]) -> "Node":
        return self.get_outer_template_helper(
            children,
            separators=self.outer_separators[role.type_],
            brackets=role.brackets,
            capfirst=role.capfirst,
        )

    def get_author_inner_template(self, role: Role) -> "Node":
        return reference[self.get_names_template_helper(role.full_authors)]

    def get_names_template_helper(self, full_authors: bool) -> "Node":
        return names(
            'author',
            sep=self.names_separators.sep,
            sep2=self.names_separators.sep2,
            last_sep=self.names_separators.last_sep,
            other=None if full_authors else self.names_separators.other,
        )

    def get_outer_template_helper(
            self, children, separators: Separators,
            brackets=False, capfirst=False) -> "Node":
        return join[
            self.left_bracket if brackets else '',
            sentence(
                capitalize=capfirst,
                add_period=False,
                sep=separators.sep,
                sep2=separators.sep2,
                last_sep=separators.last_sep,
                other=separators.other,
            )[children],
            self.right_bracket if brackets else '',
        ]
