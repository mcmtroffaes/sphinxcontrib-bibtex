import dataclasses
from abc import ABC

from pybtex.plugin import Plugin
from pybtex.richtext import Text, BaseMultipartText, Tag
from pybtex.style.template import node, _format_list, FieldIsMissing
from typing import (
    TYPE_CHECKING, TypeVar, Generic, Tuple, List, Union, NamedTuple
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


class Separators(NamedTuple):
    sep: Union["BaseText", str] = ''
    sep2: Optional[Union["BaseText", str]] = None
    last_sep: Optional[Union["BaseText", str]] = None
    other: Optional[Union["BaseText", str]] = None


@dataclasses.dataclass(frozen=True)
class BaseReferenceStyle(Plugin, Generic[ReferenceInfo]):
    """Abstract base class for reference styles.
    Custom styles can override the outer and inner templates.
    """

    #: Rich text class used for rendering references.
    ReferenceText: Type[BaseReferenceText[ReferenceInfo]]

    # see https://stackoverflow.com/a/59987363 as to why this is here
    def __post_init__(self):
        pass

    def get_role_names(self) -> Iterable[str]:
        """Get list of role names supported by this style."""
        raise NotImplementedError

    def format_references(
            self, role_name: str,
            references: Iterable[Tuple[
                "Entry", "FormattedEntry", ReferenceInfo]],
            ) -> "BaseText":
        """Format the list of references according to the given role.

        First formats each reference using the :meth:`get_inner_template`,
        then joins all these formatted references together using
        :meth:`get_outer_template`.
        """
        children = [
            self.get_inner_template(role_name).format_data(
                data=dict(
                    entry=entry,
                    formatted_entry=formatted_entry,
                    style=self,
                    reference_info=info))
            for entry, formatted_entry, info in references]
        return self.get_outer_template(role_name, children).format()

    def get_outer_template(
            self, role_name: str, children: List["BaseText"]) -> "Node":
        """The outer template for formatting the references.

        .. seealso::

            Standard implementations should normally implement this method
            by calling
            :meth:`BaseStandardReferenceStyle.get_standard_outer_template`
            with the appropriate arguments.
        """
        raise NotImplementedError

    def get_inner_template(self, role_name: str) -> "Node":
        """The inner template for formatting the references."""
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class BaseStandardReferenceStyle(BaseReferenceStyle[ReferenceInfo], ABC):
    """Helper base class for reference styles.
    This class has additional data and helper functions
    to facilitate implementing the outer and inner templates.
    """

    #: Style used for formatting author names.
    name_style: "BaseNameStyle" = dataclasses.field(
        default_factory=lambda: LastNameStyle())

    #: Whether or not to abbreviate first names.
    abbreviate_names: bool = True

    #: Left bracket.
    left_bracket: Union["BaseText", str] = '['

    #: Right bracket.
    right_bracket: Union["BaseText", str] = ']'

    #: Separators used for outer template (i.e. in between references
    #: if multiple keys are referenced in a single citation).
    outer_separators: Separators = dataclasses.field(
        default_factory=lambda: Separators(sep=', ')
    )

    #: Inner template typically has some field value or names.
    #: Generally, only names use separators, and these are stored here.
    names_separators: Separators = dataclasses.field(
        default_factory=lambda: Separators(
            sep=', ', sep2=' and ', last_sep=', and ',
            other=Text(' ', Tag('em', 'et al.')))
    )

    def get_author_template(self, full_authors: bool) -> "Node":
        """Returns a template formatting the authors with correct separators
        and using the full author list if so requested.
        """
        return names(
            'author',
            sep=self.names_separators.sep,
            sep2=self.names_separators.sep2,
            last_sep=self.names_separators.last_sep,
            other=None if full_authors else self.names_separators.other,
        )

    def get_standard_outer_template(
            self, children: List["BaseText"],
            brackets=False, capfirst=False) -> "Node":
        """A helper function for creating an outer template.

        Formats *children* using :attr:`outer_separators`,
        adding :attr:`left_bracket` and :attr:`right_bracket` if requested,
        and capitalizing the first word if requested.
        """
        return join[
            self.left_bracket if brackets else '',
            sentence(
                capfirst=capfirst,
                add_period=False,
                sep=self.outer_separators.sep,
                sep2=self.outer_separators.sep2,
                last_sep=self.outer_separators.last_sep,
                other=self.outer_separators.other,
            )[children],
            self.right_bracket if brackets else '',
        ]
