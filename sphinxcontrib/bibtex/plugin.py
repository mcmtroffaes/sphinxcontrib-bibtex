import pkg_resources
from pybtex.plugin import _FakeEntryPoint
from typing import Type, Any, Dict


def find_plugin(group: str, name: str) -> Type[Any]:
    """Load a sphinxcontrib-bibtex plugin."""
    dist = pkg_resources.get_distribution('sphinxcontrib-bibtex')
    if group not in dist.get_entry_map():
        raise ImportError(f"plugin group {group} not found")
    for entry_point in pkg_resources.iter_entry_points(group, name):
        return entry_point.load()
    raise ImportError(f"plugin {group}.{name} not found")


def register_plugin(group: str, name: str, klass: Type[Any],
                    force: bool = False) -> bool:
    """Register a sphinxcontrib-bibtex plugin at runtime."""
    dist = pkg_resources.get_distribution('sphinxcontrib-bibtex')
    entry_map: Dict[str, Dict[str, pkg_resources.EntryPoint]] \
        = dist.get_entry_map()
    try:
        entry_points = entry_map[group]
    except KeyError:
        raise ImportError(f"plugin group {group} not found")
    if name not in entry_points or force:
        entry_points[name] = _FakeEntryPoint(name, klass)
        return True
    else:
        return False
