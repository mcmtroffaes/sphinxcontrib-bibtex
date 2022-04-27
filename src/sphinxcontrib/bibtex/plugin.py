import sys
if sys.version_info >= (3, 8):
    from importlib.metadata import entry_points
else:
    from importlib_metadata import entry_points
from typing import Type, Any, Dict


_runtime_plugins: Dict[str, Dict[str, Type]] = {
    'sphinxcontrib.bibtex.style.referencing': {}}


def find_plugin(group: str, name: str) -> Type[Any]:
    """Load a sphinxcontrib-bibtex plugin."""
    global _runtime_plugins
    if group not in _runtime_plugins:
        raise ImportError(f"plugin group {group} not found")
    try:
        return _runtime_plugins[group][name]
    except KeyError:
        for entry_point in entry_points(group=group, name=name):
            return entry_point.load()
    raise ImportError(f"plugin {group}.{name} not found")


def register_plugin(group: str, name: str, klass: Type[Any],
                    force: bool = False) -> bool:
    """Register a sphinxcontrib-bibtex plugin at runtime."""
    global _runtime_plugins
    if group not in _runtime_plugins:
        raise ImportError(f"plugin group {group} not found")
    try:
        eps = [_runtime_plugins[group][name]]
    except KeyError:
        eps = entry_points(group=group, name=name)
    if not eps or force:
        _runtime_plugins[group][name] = klass
        return True
    else:
        return False
