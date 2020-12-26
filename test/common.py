"""Some common helper functions for the test suite."""

import re


def html_citation_refs(name='.*', label='.*'):
    return re.compile(
        '<a class="reference internal" href="#bibtex-citation-{0}">'
        '<span>{1}</span>'
        '</a>'.format(name, label))


def html_citations(name=r'\w+', label=r'\w+', text='.*'):
    return re.compile(
        r'<dt class="label" id="bibtex-citation-(?P<name>{0})">'
        r'<span class="brackets">'
        r'(?:<a class="fn-backref" href="(?P<backref>#\w+)">)?'
        r'(?P<label>{1})'
        r'(?:</a>)?'
        r'</span>'
        r'(?:<span class="fn-backref">\('
        r'<a href="#(?P<backref1>\w+)">1</a>'
        r',<a href="#(?P<backref2>\w+)">2</a>'
        r'(,<a href="#(?P<backref3>\w+)">3</a>)?'
        r'(,<a href="#\w+">\d+</a>)*'  # no named group for additional backrefs
        r'\)</span>)?'
        r'</dt>\n'
        r'<dd><p>(?P<text>{2})</p>\n</dd>'.format(name, label, text))


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
