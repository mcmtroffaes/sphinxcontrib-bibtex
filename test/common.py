"""Some common helper functions for the test suite."""

import re
from typing import Optional

RE_ID = r"[a-z][-?a-z0-9]*"
RE_NUM = r"\d+"
RE_LABEL = r"[^<]+"
RE_TEXT = r".*"
RE_DOCNAME = r"[^:]+"
RE_TITLE = r'[^"]*'


def html_citation_refs(refid=RE_ID, label=RE_LABEL, title: Optional[str] = RE_TITLE):
    title_pattern = rf' title="(?P<title>{title})"' if title is not None else ""
    return re.compile(
        r'<a class="reference internal"'
        r' href="(?P<refdoc>[^#]+)?#(?P<refid>{refid})"'
        r"{title_pattern}"
        r">"
        r"(?P<label>{label})"
        r"</a>".format(refid=refid, label=label, title_pattern=title_pattern)
    )


# match single citation with square brackets
# also gets the id of the citation itself (which will appear in backref)
def html_citation_refs_single(
    id_=RE_ID, refid=RE_ID, label=RE_LABEL, title: Optional[str] = RE_TITLE
):
    title_pattern = rf' title="{title}"' if title is not None else ""
    return re.compile(
        r'<span class="bibtex-citation" id="(?P<id_>{id_})">\['
        r'<a class="reference internal"'
        r' href="(?P<refdoc>[^#]+)?#(?P<refid>{refid})"'
        r"{title_pattern}"
        r">"
        r"(?P<label>{label})"
        r"</a>"
        r"]</span>".format(
            id_=id_, refid=refid, label=label, title_pattern=title_pattern
        )
    )


def html_docutils_citation_refs(refid=RE_ID, label=RE_LABEL, id_=RE_ID):
    return re.compile(
        r'<a class="reference internal" '
        r'href="(?P<refdoc>[^#]+)?#(?P<refid>{refid})" '
        r'id="(?P<id_>{id_})">'
        r"<span>\[(?P<label>{label})]</span>"
        r"</a>".format(refid=refid, label=label, id_=id_)
    )


def html_citations(id_=RE_ID, label=RE_LABEL, text=RE_TEXT):
    return re.compile(
        r'<div class="citation" id="(?P<id_>{id_})"'
        r' role="doc-biblioentry">\s*'
        r'<span class="label">'
        r'<span class="fn-bracket">\[</span>'
        r'(?:<a role="doc-backlink" href="#(?P<backref>{backref_id})">)?'
        r"(?P<label>{label})"
        r"(?:</a>)?"
        r'<span class="fn-bracket">]</span>'
        r"</span>\s*"
        r'(?:<span class="backrefs">\('
        r'<a {back_role} href="#(?P<backref1>{backref_id})">1</a>'
        r',<a {back_role} href="#(?P<backref2>{backref_id}\w+)">2</a>'
        r'(,<a {back_role} href="#(?P<backref3>{backref_id}\w+)">3</a>)?'
        r'(,<a {back_role} href="#\w+">\d+</a>)*'
        r"\)</span>\s*)?"
        r"<p>(?P<text>{text})</p>\s*"
        r"</div>".format(
            back_role='role="doc-backlink"',
            id_=id_,
            label=label,
            text=text,
            backref_id=RE_ID,
        )
    )


def html_footnote_refs(refid=RE_ID):
    return re.compile(
        r'<a class="footnote-reference brackets" '
        r'href="#(?P<refid>{refid})" id="(?P<id_>{id_})" '
        r'role="doc-noteref">'
        r'<span class="fn-bracket">\[</span>'
        r"(?P<label>{label})"
        r'<span class="fn-bracket">]</span>'
        r"</a>".format(refid=refid, id_=RE_ID, label=RE_NUM)
    )


def html_footnotes(id_=RE_ID, text=RE_TEXT):
    return re.compile(
        r'<aside class="footnote brackets" id="(?P<id_>{id_})"'
        r" {foot_role}>\s*"
        r'<span class="label">'
        r'<span class="fn-bracket">\[</span>'
        r'(?:<a {back_role} href="#(?P<backref>{backref_id})">)?'
        r"{label}"
        r"(?:</a>)?"
        r'<span class="fn-bracket">]</span>'
        r"</span>\s*"
        r'(?:<span class="backrefs">\('
        r'<a {back_role} href="#(?P<backref1>{backref_id})">1</a>'
        r',<a {back_role} href="#(?P<backref2>{backref_id}\w+)">2</a>'
        r'(,<a {back_role} href="#(?P<backref3>{backref_id}\w+)">3</a>)?'
        r'(,<a {back_role} href="#\w+">\d+</a>)*'
        r"\)</span>\s*)?"
        r"<p>(?P<text>{text})</p>\s*"
        r"</aside>".format(
            foot_role='role="doc-footnote"',
            back_role='role="doc-backlink"',
            id_=id_,
            label=RE_NUM,
            text=text,
            backref_id=RE_ID,
        )
    )


def latex_citations(docname=RE_DOCNAME, id_=RE_ID, label=RE_LABEL, text=RE_TEXT):
    return re.compile(
        r"\\bibitem\[(?P<label>{label})]"
        r"{{(?P<docname>{docname}):(?P<id_>{id_})}}\n"
        r"\\sphinxAtStartPar\n"
        r"(?P<text>{text})\n".format(docname=docname, label=label, id_=id_, text=text)
    )


def latex_citation_refs(docname=RE_DOCNAME, refid=RE_ID):
    return re.compile(
        rf"\\hyperlink{{cite[.](?P<docname>{docname}):(?P<refid>{refid})}}"
    )
