import dataclasses
from abc import ABC

import pybtex.plugin
from pybtex.richtext import Text, Tag
from sphinxcontrib.bibtex.richtext import ReferenceInfo, BaseReferenceText
from sphinxcontrib.bibtex.style.template import names, sentence, join
from typing import (
    TYPE_CHECKING, Generic, Tuple, List, Union, NamedTuple
)
from typing import Iterable, Optional, Type, Dict

if TYPE_CHECKING:
    from pybtex.database import Entry
    from pybtex.richtext import BaseText
    from pybtex.style import FormattedEntry
    from pybtex.style.names import BaseNameStyle
    from pybtex.style.template import Node


class Separators(NamedTuple):
    sep: Union["BaseText", str] = ''
    sep2: Optional[Union["BaseText", str]] = None
    last_sep: Optional[Union["BaseText", str]] = None
    other: Optional[Union["BaseText", str]] = None


@dataclasses.dataclass(frozen=True)
class BaseReferenceStyle(Generic[ReferenceInfo], ABC):
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
    This class provides brackets, as well as separators
    and a function to facilitate formatting of the outer template.
    """

    #: Left bracket.
    left_bracket: Union["BaseText", str] = '['

    #: Right bracket.
    right_bracket: Union["BaseText", str] = ']'

    #: Separators used for outer template (i.e. in between references
    #: if multiple keys are referenced in a single citation).
    outer_separators: Separators = Separators(', ')

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


@dataclasses.dataclass(frozen=True)
class BaseNamesReferenceStyle(BaseReferenceStyle[ReferenceInfo], ABC):
    """Helper base class for reference styles.
    This class has additional data and helper functions
    to facilitate formatting of author names.
    """

    #: Plugin name of the style used for formatting author names.
    name_style_plugin: str = 'last'

    #: Style used for formatting author names. Loaded from name_style_plugin.
    name_style: "BaseNameStyle" = dataclasses.field(init=False)

    #: Whether or not to abbreviate first names.
    abbreviate_names: bool = True

    #: Inner template typically has some field value or names.
    #: Generally, only names use separators, and these are stored here.
    names_separators: Separators = Separators(
            sep=', ', sep2=' and ', last_sep=', and ',
            other=Text(' ', Tag('em', 'et al.')))

    def __post_init__(self):
        super().__post_init__()
        object.__setattr__(
            self, 'name_style', pybtex.plugin.find_plugin(
                'pybtex.style.names', name=self.name_style_plugin)())

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


# not an ABC, could be used directly if desired
@dataclasses.dataclass(frozen=True)
class BaseGroupReferenceStyle(BaseReferenceStyle[ReferenceInfo]):
    """Composes a group of reference styles into a single consistent style."""

    #: List of style types.
    styles: List[BaseReferenceStyle[ReferenceInfo]] \
        = dataclasses.field(default_factory=list)

    #: Dictionary from role names to styles.
    #: Automatically initialized from :attr:`styles`.
    role_style: Dict[str, BaseReferenceStyle[ReferenceInfo]] \
        = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        super().__post_init__()
        self.role_style.update(
            (role_name, style)
            for style in self.styles
            for role_name in style.get_role_names()
        )

    def get_role_names(self):
        return self.role_style.keys()

    def get_outer_template(
            self, role_name: str, children: List["BaseText"]) -> "Node":
        """Gets the outer template associated with *role_name*
        in one of the :attr:`styles`.
        """
        style = self.role_style[role_name]
        return style.get_outer_template(role_name, children)

    def get_inner_template(self, role_name: str) -> "Node":
        """Gets the inner template associated with *role_name*
        in one of the :attr:`styles`.
        """
        style = self.role_style[role_name]
        return style.get_inner_template(role_name)
