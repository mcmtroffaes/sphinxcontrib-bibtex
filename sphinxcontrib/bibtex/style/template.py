from pybtex.richtext import Text
from pybtex.style.template import node, _format_list, FieldIsMissing
from typing import TYPE_CHECKING, Dict, Any, cast

if TYPE_CHECKING:
    from pybtex.richtext import BaseText
    from pybtex.style import FormattedEntry
    from sphinxcontrib.bibtex.style.referencing import BaseReferenceStyle


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
    formatted_names = [
        style.name_style_plugin.format(person, style.abbreviate_names)
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
    The data must also contain a *style* key pointing to the corresponding
    :class:`~sphinxcontrib.bibtex.style.referencing.BaseReferenceStyle`.
    """
    parts = _format_list(children, data)
    style = cast("BaseReferenceStyle", data['style'])
    info = data['reference_info']
    return style.ReferenceText(info, *parts)