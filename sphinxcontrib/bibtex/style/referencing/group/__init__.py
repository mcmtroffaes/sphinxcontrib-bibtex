import dataclasses
from typing import List, Dict, TYPE_CHECKING

from .. import ReferenceInfo, BaseReferenceStyle

if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style.template import Node


@dataclasses.dataclass(frozen=True)
class GroupReferenceStyle(BaseReferenceStyle[ReferenceInfo]):
    """Composes a group of reference styles into a single consistent style."""

    #: List of style types.
    styles: List[BaseReferenceStyle[ReferenceInfo]]

    #: Dictionary from role names to styles.
    #: Automatically initialized from :attr:`styles`.
    role_style: Dict[str, BaseReferenceStyle[ReferenceInfo]]

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
