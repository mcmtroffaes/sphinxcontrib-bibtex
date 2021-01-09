from pybtex.plugin import Plugin, find_plugin
from pybtex.richtext import Text, BaseMultipartText
from pybtex.style.template import node, _format_list
from typing import TYPE_CHECKING, TypeVar, Generic, Tuple, List, Union
from typing import Iterable, Optional, cast, Any, Type, Dict

from sphinxcontrib.bibtex.style.names.last import NameStyle as LastNameStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style import FormattedEntry
    from pybtex.style.names import BaseNameStyle
    from pybtex.style.template import Node


ReferenceInfo = TypeVar('ReferenceInfo')
"""Generic type parameter for types that store reference information.
To be implemented by clients; see for instance :class:`SphinxReferenceInfo`.
"""


@node
def label(children, data) -> "BaseText":
    """Node for inserting the label of a formatted entry."""
    assert not children
    entry = cast("FormattedEntry", data['entry'])
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
    style = cast(BaseReferenceStyle[ReferenceInfo], data['style'])
    info: ReferenceInfo = data['reference_info']
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


class BaseReferenceStyle(Plugin, Generic[ReferenceInfo]):
    """Base class for reference styles.
    Custom styles can override the outer and inner templates.
    """

    ReferenceText: Type[BaseReferenceText[ReferenceInfo]]
    default_name_style: Union[str, "BaseNameStyle"] = LastNameStyle
    left_bracket = '['
    right_bracket = ']'

    def __init__(
            self, reference_text_type: Type[BaseReferenceText[ReferenceInfo]],
            name_style: Optional[Union[str, "BaseNameStyle"]] = None):
        super().__init__()
        self.ReferenceText = reference_text_type
        self.name_style: "BaseNameStyle" = find_plugin(
            'pybtex.style.names', name_style or self.default_name_style)()

    def _data_from_references(
            self,
            references: Iterable[Tuple["FormattedEntry", ReferenceInfo]]
            ) -> Dict[str, Any]:
        for entry, info in references:
            yield dict(entry=entry, style=self, reference_info=info)

    def format_references(
            self,
            references: Iterable[Tuple["FormattedEntry", ReferenceInfo]],
            capfirst=False) -> "BaseText":
        children = [self.get_inner_template().format_data(data)
                    for data in self._data_from_references(references)]
        return self.get_outer_template(children, capfirst=capfirst).format()

    def get_outer_template(
            self, children: List["BaseText"], capfirst=False) -> "Node":
        raise NotImplementedError

    def get_inner_template(self) -> "Node":
        raise NotImplementedError
