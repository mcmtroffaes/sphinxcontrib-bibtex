"""Some common helper functions for the test suite."""

import re


def html_citation_refs(name='.*', label='.*'):
    return re.compile(
        '<a class="reference internal" href="#bibtex-citation-{0}">'
        '<span>{1}</span>'
        '</a>'.format(name, label))


def html_citations(name='.*', label='.*'):
    return re.compile(
        '<dt class="label" id="bibtex-citation-{0}">'
        '<span class="brackets">{1}</span>'
        '</dt>'.format(name, label))


def html_footnote_refs(name='.*', id_='.*', num='.*'):
    return re.compile(
        '<a class="footnote-reference brackets" href="#{0}" id="{1}">'
        '{2}'
        '</a>'.format(name, id_, num))


def html_footnotes(name='.*', id_='.*', num='.*'):
    return re.compile(
        '<dt class="label" id="{0}">'
        '<span class="brackets"><a class="fn-backref" href="#{1}">'
        '{2}'
        '</a>'
        '</span>'
        '</dt>'.format(name, id_, num))
