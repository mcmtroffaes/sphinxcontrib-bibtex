"""Some common helper functions for the test suite."""

import re
import sphinx

RE_ID = r'[a-z][-?a-z0-9]*'
RE_NUM = r'\d+'
RE_LABEL = r'[^<]+'
RE_TEXT = r'.*'
RE_DOCNAME = r'[^:]+'
RE_TITLE = r'[^"]*'


def html_citation_refs(refid=RE_ID, label=RE_LABEL, title=RE_TITLE):
    return re.compile(
        r'<a class="reference internal" '
        r'href="(?P<refdoc>[^#]+)?#(?P<refid>{refid})" '
        r'title="{title}">'
        r'(?P<label>{label})'
        r'</a>'.format(refid=refid, label=label, title=title))


def html_citations(id_=RE_ID, label=RE_LABEL, text=RE_TEXT):
    return re.compile(
        r'<dt class="label" id="(?P<id_>{id_})">'
        r'<span class="brackets">'
        r'(?:<a class="fn-backref" href="#(?P<backref>{backref_id})">)?'
        r'(?P<label>{label})'
        r'(?:</a>)?'
        r'</span>'
        r'(?:<span class="fn-backref">\('
        r'<a href="#(?P<backref1>{backref_id})">1</a>'
        r',<a href="#(?P<backref2>{backref_id}\w+)">2</a>'
        r'(,<a href="#(?P<backref3>{backref_id}\w+)">3</a>)?'
        r'(,<a href="#\w+">\d+</a>)*'  # no named group for additional backrefs
        r'\)</span>)?'
        r'</dt>\n'
        r'<dd><p>(?P<text>{text})</p>\n</dd>'.format(
            id_=id_, label=label, text=text, backref_id=RE_ID))


def html_footnote_refs(refid=RE_ID):
    return re.compile(
        r'<a class="footnote-reference brackets"'
        r' href="#(?P<refid>{refid})" id="(?P<id_>{id_})">'
        r'(?P<label>{label})'
        r'</a>'.format(refid=refid, id_=RE_ID, label=RE_NUM))


def html_footnotes(id_=RE_ID, text=RE_TEXT):
    return re.compile(
        r'<dt class="label" id="(?P<id_>{id_})">'
        r'<span class="brackets">'
        r'(?:<a class="fn-backref" href="#(?P<backref>{backref_id})">)?'
        r'(?P<label>{label})'
        r'(?:</a>)?'
        r'</span>'
        r'(?:<span class="fn-backref">\('
        r'<a href="#(?P<backref1>{backref_id})">1</a>'
        r',<a href="#(?P<backref2>{backref_id}\w+)">2</a>'
        r'(,<a href="#(?P<backref3>{backref_id}\w+)">3</a>)?'
        r'(,<a href="#\w+">\d+</a>)*'  # no named group for additional backrefs
        r'\)</span>)?'
        r'</dt>\n'
        r'<dd><p>(?P<text>{text})</p>\n</dd>'.format(
            id_=id_, backref_id=RE_ID, label=RE_NUM, text=text))


def latex_citations(docname=RE_DOCNAME, id_=RE_ID,
                    label=RE_LABEL, text=RE_TEXT):
    if sphinx.version_info < (3, 5):
        return re.compile(
            r'\\bibitem\[(?P<label>{label})]'
            r'{{(?P<docname>{docname}):(?P<id_>{id_})}}\n'
            r'(?P<text>{text})\n'.format(
                docname=docname, label=label, id_=id_, text=text))
    else:
        return re.compile(
            r'\\bibitem\[(?P<label>{label})]'
            r'{{(?P<docname>{docname}):(?P<id_>{id_})}}\n'
            r'\\sphinxAtStartPar\n'
            r'(?P<text>{text})\n'.format(
                docname=docname, label=label, id_=id_, text=text))


def latex_citation_refs(docname=RE_DOCNAME, refid=RE_ID):
    return re.compile(
        rf'\\hyperlink{{cite[.](?P<docname>{docname}):(?P<refid>{refid})}}')
