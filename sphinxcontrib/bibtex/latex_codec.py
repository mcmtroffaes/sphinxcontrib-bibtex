# -*- coding: utf-8 -*-
"""
Character translation utilities for LaTeX-formatted text
========================================================

Usage:
 - unicode(string,'latex')
 - ustring.decode('latex')
are both available just by letting "import latex" find this file.
 - unicode(string,'latex+latin1')
 - ustring.decode('latex+latin1')
where latin1 can be replaced by any other known encoding, also
become available by calling latex.register().



Copyright (c) 2003, 2008 David Eppstein
Copyright (c) 2011 Matthias C. M. Troffaes

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import print_function

import codecs
import collections
import re

from sphinxcontrib.bibtex import latex_lexer

def register():
    """Enable encodings of the form 'latex+x' where x describes another encoding.
    Unicode characters are translated to or from x when possible, otherwise
    expanded to latex.
    """
    codecs.register(find_latex)

# returns the codec search function
# this is used if latex_codec.py were to be placed in stdlib
def getregentry():
    """Encodings module API."""
    return find_latex('latex')

class LatexUnicodeTable:
    """Tabulates a translation between latex and unicode."""

    def __init__(self, lexer):
        self.lexer = lexer
        self.unicode_map = {}
        self.max_length = 0
        self.latex_map = {}
        self.register_all()

    def register_all(self):
        # TODO complete this list
        # register special symbols
        self.register(u'\N{EN DASH}', b'--')
        self.register(u'\N{EN DASH}', b'\\textendash')
        self.register(u'\N{EM DASH}', b'---')
        self.register(u'\N{EM DASH}', b'\\textemdash')
        self.register(u'\N{LEFT SINGLE QUOTATION MARK}', b'`', decode=False)
        self.register(u'\N{RIGHT SINGLE QUOTATION MARK}', b"'", decode=False)
        self.register(u'\N{LEFT DOUBLE QUOTATION MARK}', b'``')
        self.register(u'\N{RIGHT DOUBLE QUOTATION MARK}', b"''")
        self.register(u'\N{DAGGER}', b'\\dag')
        self.register(u'\N{DOUBLE DAGGER}', b'\\ddag')

        self.register(u'\N{BULLET}', b'\\bullet', mode='math')
        self.register(u'\N{BULLET}', b'\\textbullet', package='textcomp')

        self.register(u'\N{NUMBER SIGN}', b'\\#')
        self.register(u'\N{AMPERSAND}', b'\\&')
        self.register(u'\N{NO-BREAK SPACE}', b'~')
        self.register(u'\N{INVERTED EXCLAMATION MARK}', b'!`')
        self.register(u'\N{CENT SIGN}', b'\\not{c}')

        self.register(u'\N{POUND SIGN}', b'\\pounds')
        self.register(u'\N{POUND SIGN}', b'\\textsterling', package='textcomp')

        self.register(u'\N{SECTION SIGN}', b'\\S')
        self.register(u'\N{DIAERESIS}', b'\\"{}')
        self.register(u'\N{NOT SIGN}', b'\\neg')
        self.register(u'\N{SOFT HYPHEN}', b'\\-')
        self.register(u'\N{MACRON}', b'\\={}')
        
        self.register(u'\N{DEGREE SIGN}', b'^\\circ', mode='math')
        self.register(u'\N{DEGREE SIGN}', b'\\textdegree', package='textcomp')
        
        self.register(u'\N{PLUS-MINUS SIGN}', b'\\pm', mode='math')
        self.register(u'\N{PLUS-MINUS SIGN}', b'\\textpm', package='textcomp')

        self.register(u'\N{SUPERSCRIPT TWO}', b'^2', mode='math')
        self.register(u'\N{SUPERSCRIPT TWO}', b'\\texttwosuperior', package='textcomp')

        self.register(u'\N{SUPERSCRIPT THREE}', b'^3', mode='math')
        self.register(u'\N{SUPERSCRIPT THREE}', b'\\textthreesuperior', package='textcomp')

        self.register(u'\N{ACUTE ACCENT}', b"\\'{}")

        self.register(u'\N{MICRO SIGN}', b'\\mu', mode='math')
        self.register(u'\N{MICRO SIGN}', b'\\micro', package='gensymb')

        self.register(u'\N{PILCROW SIGN}', b'\\P')

        self.register(u'\N{MIDDLE DOT}', b'\\cdot', mode='math')
        self.register(u'\N{MIDDLE DOT}', b'\\textperiodcentered', package='textcomp')

        self.register(u'\N{CEDILLA}', b'\\c{}')

        self.register(u'\N{SUPERSCRIPT ONE}', b'^1', mode='math')
        self.register(u'\N{SUPERSCRIPT ONE}', b'\\textonesuperior', package='textcomp')

        self.register(u'\N{INVERTED QUESTION MARK}', b'?`')
        self.register(u'\N{LATIN CAPITAL LETTER A WITH GRAVE}', b'\\`A')
        self.register(u'\N{LATIN CAPITAL LETTER A WITH CIRCUMFLEX}', b'\\^A')
        self.register(u'\N{LATIN CAPITAL LETTER A WITH TILDE}', b'\\~A')
        self.register(u'\N{LATIN CAPITAL LETTER A WITH DIAERESIS}', b'\\"A')
        self.register(u'\N{LATIN CAPITAL LETTER A WITH RING ABOVE}', b'\\AA')
        self.register(u'\N{LATIN CAPITAL LETTER AE}', b'\\AE')
        self.register(u'\N{LATIN CAPITAL LETTER C WITH CEDILLA}', b'\\c C')
        self.register(u'\N{LATIN CAPITAL LETTER E WITH GRAVE}', b'\\`E')
        self.register(u'\N{LATIN CAPITAL LETTER E WITH ACUTE}', b"\\'E")
        self.register(u'\N{LATIN CAPITAL LETTER E WITH CIRCUMFLEX}', b'\\^E')
        self.register(u'\N{LATIN CAPITAL LETTER E WITH DIAERESIS}', b'\\"E')
        self.register(u'\N{LATIN CAPITAL LETTER I WITH GRAVE}', b'\\`I')
        self.register(u'\N{LATIN CAPITAL LETTER I WITH CIRCUMFLEX}', b'\\^I')
        self.register(u'\N{LATIN CAPITAL LETTER I WITH DIAERESIS}', b'\\"I')
        self.register(u'\N{LATIN CAPITAL LETTER N WITH TILDE}', b'\\~N')
        self.register(u'\N{LATIN CAPITAL LETTER O WITH GRAVE}', b'\\`O')
        self.register(u'\N{LATIN CAPITAL LETTER O WITH ACUTE}', b"\\'O")
        self.register(u'\N{LATIN CAPITAL LETTER O WITH CIRCUMFLEX}', b'\\^O')
        self.register(u'\N{LATIN CAPITAL LETTER O WITH TILDE}', b'\\~O')
        self.register(u'\N{LATIN CAPITAL LETTER O WITH DIAERESIS}', b'\\"O')
        self.register(u'\N{MULTIPLICATION SIGN}', b'\\times', mode='math')
        self.register(u'\N{LATIN CAPITAL LETTER O WITH STROKE}', b'\\O')
        self.register(u'\N{LATIN CAPITAL LETTER U WITH GRAVE}', b'\\`U')
        self.register(u'\N{LATIN CAPITAL LETTER U WITH ACUTE}', b"\\'U")
        self.register(u'\N{LATIN CAPITAL LETTER U WITH CIRCUMFLEX}', b'\\^U')
        self.register(u'\N{LATIN CAPITAL LETTER U WITH DIAERESIS}', b'\\"U')
        self.register(u'\N{LATIN CAPITAL LETTER Y WITH ACUTE}', b"\\'Y")
        self.register(u'\N{LATIN SMALL LETTER SHARP S}', b'\\ss')
        self.register(u'\N{LATIN SMALL LETTER A WITH GRAVE}', b'\\`a')
        self.register(u'\N{LATIN SMALL LETTER A WITH ACUTE}', b"\\'a")
        self.register(u'\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}', b'\\^a')
        self.register(u'\N{LATIN SMALL LETTER A WITH TILDE}', b'\\~a')
        self.register(u'\N{LATIN SMALL LETTER A WITH DIAERESIS}', b'\\"a')
        self.register(u'\N{LATIN SMALL LETTER A WITH RING ABOVE}', b'\\aa')
        self.register(u'\N{LATIN SMALL LETTER AE}', b'\\ae')
        self.register(u'\N{LATIN SMALL LETTER C WITH CEDILLA}', b'\\c c')
        self.register(u'\N{LATIN SMALL LETTER E WITH GRAVE}', b'\\`e')
        self.register(u'\N{LATIN SMALL LETTER E WITH ACUTE}', b"\\'e")
        self.register(u'\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}', b'\\^e')
        self.register(u'\N{LATIN SMALL LETTER E WITH DIAERESIS}', b'\\"e')
        self.register(u'\N{LATIN SMALL LETTER I WITH GRAVE}', b'\\`\\i')
        self.register(u'\N{LATIN SMALL LETTER I WITH GRAVE}', b'\\`i')
        self.register(u'\N{LATIN SMALL LETTER I WITH ACUTE}', b"\\'\\i")
        self.register(u'\N{LATIN SMALL LETTER I WITH ACUTE}', b"\\'i")
        self.register(u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}', b'\\^\\i')
        self.register(u'\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}', b'\\^i')
        self.register(u'\N{LATIN SMALL LETTER I WITH DIAERESIS}', b'\\"\\i')
        self.register(u'\N{LATIN SMALL LETTER I WITH DIAERESIS}', b'\\"i')
        self.register(u'\N{LATIN SMALL LETTER N WITH TILDE}', b'\\~n')
        self.register(u'\N{LATIN SMALL LETTER O WITH GRAVE}', b'\\`o')
        self.register(u'\N{LATIN SMALL LETTER O WITH ACUTE}', b"\\'o")
        self.register(u'\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}', b'\\^o')
        self.register(u'\N{LATIN SMALL LETTER O WITH TILDE}', b'\\~o')
        self.register(u'\N{LATIN SMALL LETTER O WITH DIAERESIS}', b'\\"o')
        self.register(u'\N{DIVISION SIGN}', b'\\div', mode='math')
        self.register(u'\N{LATIN SMALL LETTER O WITH STROKE}', b'\\o')
        self.register(u'\N{LATIN SMALL LETTER U WITH GRAVE}', b'\\`u')
        self.register(u'\N{LATIN SMALL LETTER U WITH ACUTE}', b"\\'u")
        self.register(u'\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}', b'\\^u')
        self.register(u'\N{LATIN SMALL LETTER U WITH DIAERESIS}', b'\\"u')
        self.register(u'\N{LATIN SMALL LETTER Y WITH ACUTE}', b"\\'y")
        self.register(u'\N{LATIN SMALL LETTER Y WITH DIAERESIS}', b'\\"y')
        self.register(u'\N{LATIN CAPITAL LETTER A WITH MACRON}', b'\\=A')
        self.register(u'\N{LATIN SMALL LETTER A WITH MACRON}', b'\\=a')
        self.register(u'\N{LATIN CAPITAL LETTER A WITH BREVE}', b'\\u A')
        self.register(u'\N{LATIN SMALL LETTER A WITH BREVE}', b'\\u a')
        self.register(u'\N{LATIN CAPITAL LETTER A WITH OGONEK}', b'\\c A')
        self.register(u'\N{LATIN SMALL LETTER A WITH OGONEK}', b'\\c a')
        self.register(u'\N{LATIN CAPITAL LETTER C WITH ACUTE}', b"\\'C")
        self.register(u'\N{LATIN SMALL LETTER C WITH ACUTE}', b"\\'c")
        self.register(u'\N{LATIN CAPITAL LETTER C WITH CIRCUMFLEX}', b'\\^C')
        self.register(u'\N{LATIN SMALL LETTER C WITH CIRCUMFLEX}', b'\\^c')
        self.register(u'\N{LATIN CAPITAL LETTER C WITH DOT ABOVE}', b'\\.C')
        self.register(u'\N{LATIN SMALL LETTER C WITH DOT ABOVE}', b'\\.c')
        self.register(u'\N{LATIN CAPITAL LETTER C WITH CARON}', b'\\v C')
        self.register(u'\N{LATIN SMALL LETTER C WITH CARON}', b'\\v c')
        self.register(u'\N{LATIN CAPITAL LETTER D WITH CARON}', b'\\v D')
        self.register(u'\N{LATIN SMALL LETTER D WITH CARON}', b'\\v d')
        self.register(u'\N{LATIN CAPITAL LETTER E WITH MACRON}', b'\\=E')
        self.register(u'\N{LATIN SMALL LETTER E WITH MACRON}', b'\\=e')
        self.register(u'\N{LATIN CAPITAL LETTER E WITH BREVE}', b'\\u E')
        self.register(u'\N{LATIN SMALL LETTER E WITH BREVE}', b'\\u e')
        self.register(u'\N{LATIN CAPITAL LETTER E WITH DOT ABOVE}', b'\\.E')
        self.register(u'\N{LATIN SMALL LETTER E WITH DOT ABOVE}', b'\\.e')
        self.register(u'\N{LATIN CAPITAL LETTER E WITH OGONEK}', b'\\c E')
        self.register(u'\N{LATIN SMALL LETTER E WITH OGONEK}', b'\\c e')
        self.register(u'\N{LATIN CAPITAL LETTER E WITH CARON}', b'\\v E')
        self.register(u'\N{LATIN SMALL LETTER E WITH CARON}', b'\\v e')
        self.register(u'\N{LATIN CAPITAL LETTER G WITH CIRCUMFLEX}', b'\\^G')
        self.register(u'\N{LATIN SMALL LETTER G WITH CIRCUMFLEX}', b'\\^g')
        self.register(u'\N{LATIN CAPITAL LETTER G WITH BREVE}', b'\\u G')
        self.register(u'\N{LATIN SMALL LETTER G WITH BREVE}', b'\\u g')
        self.register(u'\N{LATIN CAPITAL LETTER G WITH DOT ABOVE}', b'\\.G')
        self.register(u'\N{LATIN SMALL LETTER G WITH DOT ABOVE}', b'\\.g')
        self.register(u'\N{LATIN CAPITAL LETTER G WITH CEDILLA}', b'\\c G')
        self.register(u'\N{LATIN SMALL LETTER G WITH CEDILLA}', b'\\c g')
        self.register(u'\N{LATIN CAPITAL LETTER H WITH CIRCUMFLEX}', b'\\^H')
        self.register(u'\N{LATIN SMALL LETTER H WITH CIRCUMFLEX}', b'\\^h')
        self.register(u'\N{LATIN CAPITAL LETTER I WITH TILDE}', b'\\~I')
        self.register(u'\N{LATIN SMALL LETTER I WITH TILDE}', b'\\~\\i')
        self.register(u'\N{LATIN SMALL LETTER I WITH TILDE}', b'\\~i')
        self.register(u'\N{LATIN CAPITAL LETTER I WITH MACRON}', b'\\=I')
        self.register(u'\N{LATIN SMALL LETTER I WITH MACRON}', b'\\=\\i')
        self.register(u'\N{LATIN SMALL LETTER I WITH MACRON}', b'\\=i')
        self.register(u'\N{LATIN CAPITAL LETTER I WITH BREVE}', b'\\u I')
        self.register(u'\N{LATIN SMALL LETTER I WITH BREVE}', b'\\u\\i')
        self.register(u'\N{LATIN SMALL LETTER I WITH BREVE}', b'\\u i')
        self.register(u'\N{LATIN CAPITAL LETTER I WITH OGONEK}', b'\\c I')
        self.register(u'\N{LATIN SMALL LETTER I WITH OGONEK}', b'\\c i')
        self.register(u'\N{LATIN CAPITAL LETTER I WITH DOT ABOVE}', b'\\.I')
        self.register(u'\N{LATIN SMALL LETTER DOTLESS I}', b'\\i')
        self.register(u'\N{LATIN CAPITAL LIGATURE IJ}', b'IJ', decode=False)
        self.register(u'\N{LATIN SMALL LIGATURE IJ}', b'ij', decode=False)
        self.register(u'\N{LATIN CAPITAL LETTER J WITH CIRCUMFLEX}', b'\\^J')
        self.register(u'\N{LATIN SMALL LETTER J WITH CIRCUMFLEX}', b'\\^\\j')
        self.register(u'\N{LATIN SMALL LETTER J WITH CIRCUMFLEX}', b'\\^j')
        self.register(u'\N{LATIN CAPITAL LETTER K WITH CEDILLA}', b'\\c K')
        self.register(u'\N{LATIN SMALL LETTER K WITH CEDILLA}', b'\\c k')
        self.register(u'\N{LATIN CAPITAL LETTER L WITH ACUTE}', b"\\'L")
        self.register(u'\N{LATIN SMALL LETTER L WITH ACUTE}', b"\\'l")
        self.register(u'\N{LATIN CAPITAL LETTER L WITH CEDILLA}', b'\\c L')
        self.register(u'\N{LATIN SMALL LETTER L WITH CEDILLA}', b'\\c l')
        self.register(u'\N{LATIN CAPITAL LETTER L WITH CARON}', b'\\v L')
        self.register(u'\N{LATIN SMALL LETTER L WITH CARON}', b'\\v l')
        self.register(u'\N{LATIN CAPITAL LETTER L WITH STROKE}', b'\\L')
        self.register(u'\N{LATIN SMALL LETTER L WITH STROKE}', b'\\l')
        self.register(u'\N{LATIN CAPITAL LETTER N WITH ACUTE}', b"\\'N")
        self.register(u'\N{LATIN SMALL LETTER N WITH ACUTE}', b"\\'n")
        self.register(u'\N{LATIN CAPITAL LETTER N WITH CEDILLA}', b'\\c N')
        self.register(u'\N{LATIN SMALL LETTER N WITH CEDILLA}', b'\\c n')
        self.register(u'\N{LATIN CAPITAL LETTER N WITH CARON}', b'\\v N')
        self.register(u'\N{LATIN SMALL LETTER N WITH CARON}', b'\\v n')
        self.register(u'\N{LATIN CAPITAL LETTER O WITH MACRON}', b'\\=O')
        self.register(u'\N{LATIN SMALL LETTER O WITH MACRON}', b'\\=o')
        self.register(u'\N{LATIN CAPITAL LETTER O WITH BREVE}', b'\\u O')
        self.register(u'\N{LATIN SMALL LETTER O WITH BREVE}', b'\\u o')
        self.register(u'\N{LATIN CAPITAL LETTER O WITH DOUBLE ACUTE}', b'\\H O')
        self.register(u'\N{LATIN SMALL LETTER O WITH DOUBLE ACUTE}', b'\\H o')
        self.register(u'\N{LATIN CAPITAL LIGATURE OE}', b'\\OE')
        self.register(u'\N{LATIN SMALL LIGATURE OE}', b'\\oe')
        self.register(u'\N{LATIN CAPITAL LETTER R WITH ACUTE}', b"\\'R")
        self.register(u'\N{LATIN SMALL LETTER R WITH ACUTE}', b"\\'r")
        self.register(u'\N{LATIN CAPITAL LETTER R WITH CEDILLA}', b'\\c R')
        self.register(u'\N{LATIN SMALL LETTER R WITH CEDILLA}', b'\\c r')
        self.register(u'\N{LATIN CAPITAL LETTER R WITH CARON}', b'\\v R')
        self.register(u'\N{LATIN SMALL LETTER R WITH CARON}', b'\\v r')
        self.register(u'\N{LATIN CAPITAL LETTER S WITH ACUTE}', b"\\'S")
        self.register(u'\N{LATIN SMALL LETTER S WITH ACUTE}', b"\\'s")
        self.register(u'\N{LATIN CAPITAL LETTER S WITH CIRCUMFLEX}', b'\\^S')
        self.register(u'\N{LATIN SMALL LETTER S WITH CIRCUMFLEX}', b'\\^s')
        self.register(u'\N{LATIN CAPITAL LETTER S WITH CEDILLA}', b'\\c S')
        self.register(u'\N{LATIN SMALL LETTER S WITH CEDILLA}', b'\\c s')
        self.register(u'\N{LATIN CAPITAL LETTER S WITH CARON}', b'\\v S')
        self.register(u'\N{LATIN SMALL LETTER S WITH CARON}', b'\\v s')
        self.register(u'\N{LATIN CAPITAL LETTER T WITH CEDILLA}', b'\\c T')
        self.register(u'\N{LATIN SMALL LETTER T WITH CEDILLA}', b'\\c t')
        self.register(u'\N{LATIN CAPITAL LETTER T WITH CARON}', b'\\v T')
        self.register(u'\N{LATIN SMALL LETTER T WITH CARON}', b'\\v t')
        self.register(u'\N{LATIN CAPITAL LETTER U WITH TILDE}', b'\\~U')
        self.register(u'\N{LATIN SMALL LETTER U WITH TILDE}', b'\\~u')
        self.register(u'\N{LATIN CAPITAL LETTER U WITH MACRON}', b'\\=U')
        self.register(u'\N{LATIN SMALL LETTER U WITH MACRON}', b'\\=u')
        self.register(u'\N{LATIN CAPITAL LETTER U WITH BREVE}', b'\\u U')
        self.register(u'\N{LATIN SMALL LETTER U WITH BREVE}', b'\\u u')
        self.register(u'\N{LATIN CAPITAL LETTER U WITH RING ABOVE}', b'\\r U')
        self.register(u'\N{LATIN SMALL LETTER U WITH RING ABOVE}', b'\\r u')
        self.register(u'\N{LATIN CAPITAL LETTER U WITH DOUBLE ACUTE}', b'\\H U')
        self.register(u'\N{LATIN SMALL LETTER U WITH DOUBLE ACUTE}', b'\\H u')
        self.register(u'\N{LATIN CAPITAL LETTER U WITH OGONEK}', b'\\c U')
        self.register(u'\N{LATIN SMALL LETTER U WITH OGONEK}', b'\\c u')
        self.register(u'\N{LATIN CAPITAL LETTER W WITH CIRCUMFLEX}', b'\\^W')
        self.register(u'\N{LATIN SMALL LETTER W WITH CIRCUMFLEX}', b'\\^w')
        self.register(u'\N{LATIN CAPITAL LETTER Y WITH CIRCUMFLEX}', b'\\^Y')
        self.register(u'\N{LATIN SMALL LETTER Y WITH CIRCUMFLEX}', b'\\^y')
        self.register(u'\N{LATIN CAPITAL LETTER Y WITH DIAERESIS}', b'\\"Y')
        self.register(u'\N{LATIN CAPITAL LETTER Z WITH ACUTE}', b"\\'Z")
        self.register(u'\N{LATIN SMALL LETTER Z WITH ACUTE}', b"\\'Z")
        self.register(u'\N{LATIN CAPITAL LETTER Z WITH DOT ABOVE}', b'\\.Z')
        self.register(u'\N{LATIN SMALL LETTER Z WITH DOT ABOVE}', b'\\.Z')
        self.register(u'\N{LATIN CAPITAL LETTER Z WITH CARON}', b'\\v Z')
        self.register(u'\N{LATIN SMALL LETTER Z WITH CARON}', b'\\v z')
        self.register(u'\N{LATIN CAPITAL LETTER DZ WITH CARON}', b'D\\v Z')
        self.register(u'\N{LATIN CAPITAL LETTER D WITH SMALL LETTER Z WITH CARON}', b'D\\v z')
        self.register(u'\N{LATIN SMALL LETTER DZ WITH CARON}', b'd\\v z')
        self.register(u'\N{LATIN CAPITAL LETTER LJ}', b'LJ', decode=False)
        self.register(u'\N{LATIN CAPITAL LETTER L WITH SMALL LETTER J}', b'Lj', decode=False)
        self.register(u'\N{LATIN SMALL LETTER LJ}', b'lj', decode=False)
        self.register(u'\N{LATIN CAPITAL LETTER NJ}', b'NJ', decode=False)
        self.register(u'\N{LATIN CAPITAL LETTER N WITH SMALL LETTER J}', b'Nj', decode=False)
        self.register(u'\N{LATIN SMALL LETTER NJ}', b'nj', decode=False)
        self.register(u'\N{LATIN CAPITAL LETTER A WITH CARON}', b'\\v A')
        self.register(u'\N{LATIN SMALL LETTER A WITH CARON}', b'\\v a')
        self.register(u'\N{LATIN CAPITAL LETTER I WITH CARON}', b'\\v I')
        self.register(u'\N{LATIN SMALL LETTER I WITH CARON}', b'\\v\\i')
        self.register(u'\N{LATIN CAPITAL LETTER O WITH CARON}', b'\\v O')
        self.register(u'\N{LATIN SMALL LETTER O WITH CARON}', b'\\v o')
        self.register(u'\N{LATIN CAPITAL LETTER U WITH CARON}', b'\\v U')
        self.register(u'\N{LATIN SMALL LETTER U WITH CARON}', b'\\v u')
        self.register(u'\N{LATIN CAPITAL LETTER G WITH CARON}', b'\\v G')
        self.register(u'\N{LATIN SMALL LETTER G WITH CARON}', b'\\v g')
        self.register(u'\N{LATIN CAPITAL LETTER K WITH CARON}', b'\\v K')
        self.register(u'\N{LATIN SMALL LETTER K WITH CARON}', b'\\v k')
        self.register(u'\N{LATIN CAPITAL LETTER O WITH OGONEK}', b'\\c O')
        self.register(u'\N{LATIN SMALL LETTER O WITH OGONEK}', b'\\c o')
        self.register(u'\N{LATIN SMALL LETTER J WITH CARON}', b'\\v\\j')
        self.register(u'\N{LATIN CAPITAL LETTER DZ}', b'DZ')
        self.register(u'\N{LATIN CAPITAL LETTER D WITH SMALL LETTER Z}', b'Dz', decode=False)
        self.register(u'\N{LATIN SMALL LETTER DZ}', b'dz', decode=False)
        self.register(u'\N{LATIN CAPITAL LETTER G WITH ACUTE}', b"\\'G")
        self.register(u'\N{LATIN SMALL LETTER G WITH ACUTE}', b"\\'g")
        self.register(u'\N{LATIN CAPITAL LETTER AE WITH ACUTE}', b"\\'\\AE")
        self.register(u'\N{LATIN SMALL LETTER AE WITH ACUTE}', b"\\'\\ae")
        self.register(u'\N{LATIN CAPITAL LETTER O WITH STROKE AND ACUTE}', b"\\'\\O")
        self.register(u'\N{LATIN SMALL LETTER O WITH STROKE AND ACUTE}', b"\\'\\o")
        self.register(u'\N{PARTIAL DIFFERENTIAL}', b'\\partial', mode='math')
        self.register(u'\N{N-ARY PRODUCT}', b'\\prod', mode='math')
        self.register(u'\N{N-ARY SUMMATION}', b'\\sum', mode='math')
        self.register(u'\N{SQUARE ROOT}', b'\\surd', mode='math')
        self.register(u'\N{INFINITY}', b'\\infty', mode='math')
        self.register(u'\N{INTEGRAL}', b'\\int', mode='math')
        self.register(u'\N{INTERSECTION}', b'\\cap', mode='math')
        self.register(u'\N{UNION}', b'\\cup', mode='math')
        self.register(u'\N{RIGHTWARDS ARROW}', b'\\rightarrow', mode='math')
        self.register(u'\N{RIGHTWARDS DOUBLE ARROW}', b'\\Rightarrow', mode='math')
        self.register(u'\N{LEFTWARDS ARROW}', b'\\leftarrow', mode='math')
        self.register(u'\N{LEFTWARDS DOUBLE ARROW}', b'\\Leftarrow', mode='math')
        self.register(u'\N{LOGICAL OR}', b'\\vee', mode='math')
        self.register(u'\N{LOGICAL AND}', b'\\wedge', mode='math')
        self.register(u'\N{ALMOST EQUAL TO}', b'\\approx', mode='math')
        self.register(u'\N{NOT EQUAL TO}', b'\\neq', mode='math')
        self.register(u'\N{LESS-THAN OR EQUAL TO}', b'\\leq', mode='math')
        self.register(u'\N{GREATER-THAN OR EQUAL TO}', b'\\geq', mode='math')
        self.register(u'\N{MODIFIER LETTER CIRCUMFLEX ACCENT}', b'\\^{}')
        self.register(u'\N{CARON}', b'\\v{}')
        self.register(u'\N{BREVE}', b'\\u{}')
        self.register(u'\N{DOT ABOVE}', b'\\.{}')
        self.register(u'\N{RING ABOVE}', b'\\r{}')
        self.register(u'\N{OGONEK}', b'\\c{}')
        self.register(u'\N{SMALL TILDE}', b'\\~{}')
        self.register(u'\N{DOUBLE ACUTE ACCENT}', b'\\H{}')
        self.register(u'\N{LATIN SMALL LIGATURE FI}', b'fi', decode=False)
        self.register(u'\N{LATIN SMALL LIGATURE FL}', b'fl', decode=False)
        self.register(u'\N{LATIN SMALL LIGATURE FF}', b'ff', decode=False)

        self.register(u'\N{GREEK SMALL LETTER ALPHA}', b'\\alpha', mode='math')
        self.register(u'\N{GREEK SMALL LETTER BETA}', b'\\beta', mode='math')
        self.register(u'\N{GREEK SMALL LETTER GAMMA}', b'\\gamma', mode='math')
        self.register(u'\N{GREEK SMALL LETTER DELTA}', b'\\delta', mode='math')
        self.register(u'\N{GREEK SMALL LETTER EPSILON}', b'\\epsilon', mode='math')
        self.register(u'\N{GREEK SMALL LETTER ZETA}', b'\\zeta', mode='math')
        self.register(u'\N{GREEK SMALL LETTER ETA}', b'\\eta', mode='math')
        self.register(u'\N{GREEK SMALL LETTER THETA}', b'\\theta', mode='math')
        self.register(u'\N{GREEK SMALL LETTER IOTA}', b'\\iota', mode='math')
        self.register(u'\N{GREEK SMALL LETTER KAPPA}', b'\\kappa', mode='math')
        self.register(u'\N{GREEK SMALL LETTER LAMDA}', b'\\lambda', mode='math') # LAMDA not LAMBDA
        self.register(u'\N{GREEK SMALL LETTER MU}', b'\\mu', mode='math')
        self.register(u'\N{GREEK SMALL LETTER NU}', b'\\nu', mode='math')
        self.register(u'\N{GREEK SMALL LETTER XI}', b'\\xi', mode='math')
        self.register(u'\N{GREEK SMALL LETTER OMICRON}', b'\\omicron', mode='math')
        self.register(u'\N{GREEK SMALL LETTER PI}', b'\\pi', mode='math')
        self.register(u'\N{GREEK SMALL LETTER RHO}', b'\\rho', mode='math')
        self.register(u'\N{GREEK SMALL LETTER SIGMA}', b'\\sigma', mode='math')
        self.register(u'\N{GREEK SMALL LETTER TAU}', b'\\tau', mode='math')
        self.register(u'\N{GREEK SMALL LETTER UPSILON}', b'\\upsilon', mode='math')
        self.register(u'\N{GREEK SMALL LETTER PHI}', b'\\phi', mode='math')
        self.register(u'\N{GREEK SMALL LETTER CHI}', b'\\chi', mode='math')
        self.register(u'\N{GREEK SMALL LETTER PSI}', b'\\psi', mode='math')
        self.register(u'\N{GREEK SMALL LETTER OMEGA}', b'\\omega', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER ALPHA}', b'\\Alpha', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER BETA}', b'\\Beta', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER GAMMA}', b'\\Gamma', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER DELTA}', b'\\Delta', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER EPSILON}', b'\\Epsilon', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER ZETA}', b'\\Zeta', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER ETA}', b'\\Eta', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER THETA}', b'\\Theta', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER IOTA}', b'\\Iota', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER KAPPA}', b'\\Kappa', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER LAMDA}', b'\\Lambda', mode='math') # LAMDA not LAMBDA
        self.register(u'\N{GREEK CAPITAL LETTER MU}', b'\\Mu', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER NU}', b'\\Nu', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER XI}', b'\\Xi', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER OMICRON}', b'\\Omicron', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER PI}', b'\\Pi', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER RHO}', b'\\Rho', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER SIGMA}', b'\\Sigma', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER TAU}', b'\\Tau', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER UPSILON}', b'\\Upsilon', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER PHI}', b'\\Phi', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER CHI}', b'\\Chi', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER PSI}', b'\\Psi', mode='math')
        self.register(u'\N{GREEK CAPITAL LETTER OMEGA}', b'\\Omega', mode='math')
        self.register(u'\N{COPYRIGHT SIGN}', b'\\copyright')
        self.register(u'\N{COPYRIGHT SIGN}', b'\\textcopyright')
        self.register(u'\N{LATIN CAPITAL LETTER A WITH ACUTE}', b"\\'A")
        self.register(u'\N{LATIN CAPITAL LETTER I WITH ACUTE}', b"\\'I")
        self.register(u'\N{HORIZONTAL ELLIPSIS}', b'\\ldots')
        self.register(u'\N{TRADE MARK SIGN}', b'^{TM}', mode='math')
        self.register(u'\N{TRADE MARK SIGN}', b'\\texttrademark', package='textcomp')

    def register(self, unicode_text, latex_text, mode='text', package=None,
                 decode=True, encode=True):
        if package is not None:
            # TODO implement packages
            pass
        if mode == 'math':
            # also register text version
            self.register(unicode_text, b'$' + latex_text + b'$', mode='text',
                          package=package, decode=decode, encode=encode)
            # XXX for the time being, we do not perform in-math substitutions
            return
        # tokenize, and register unicode translation
        tokens = tuple(self.lexer.get_tokens(latex_text, final=True))
        if decode:
            self.max_length = max(self.max_length, len(tokens))
            if not tokens in self.unicode_map:
                self.unicode_map[tokens] = unicode_text
            # also register token variant with brackets, if appropriate
            # for instance, "\'{e}" for "\'e", "\c{c}" for "\c c", etc.
            # note: we do not remove brackets (they sometimes matter,
            # e.g. bibtex uses them to prevent lower case transformation)
            if (len(tokens) == 2
                and tokens[0].name.startswith('control')
                and tokens[1].name == 'chars'):
                alt_tokens = (
                    tokens[0], latex_lexer.Token('chars', b'{'),
                    tokens[1], latex_lexer.Token('chars', b'}'),
                    )
                if not alt_tokens in self.unicode_map:
                    self.unicode_map[alt_tokens] = u"{" + unicode_text + u"}"
        if encode and unicode_text not in self.latex_map:
            self.latex_map[unicode_text] = (latex_text, tokens)

_LATEX_UNICODE_TABLE = LatexUnicodeTable(latex_lexer.LatexIncrementalDecoder())

# incremental encoder does not need a buffer
# but decoder does

class LatexIncrementalEncoder(latex_lexer.LatexIncrementalEncoder):
    """Translating incremental encoder for latex. Maintains a state to
    determine whether control spaces etc. need to be inserted.
    """

    table = _LATEX_UNICODE_TABLE
    """Translation table."""

    def __init__(self, errors='strict'):
        latex_lexer.LatexIncrementalEncoder.__init__(self, errors=errors)
        self.reset()

    def reset(self):
        self.state = 'M'

    def get_space_bytes(self, bytes_):
        """Inserts space bytes in space eating mode."""
        if self.state == 'S':
            # in space eating mode
            # control space needed?
            if bytes_.startswith(b' '):
                # replace by control space
                return b'\\ ', bytes_[1:]
            else:
                # insert space (it is eaten, but needed for separation)
                return b' ', bytes_
        else:
            return b'', bytes_

    def get_latex_bytes(self, unicode_, final=False):
        """:meth:`encode` calls this function to produce the final
        sequence of latex bytes. This implementation simply
        encodes every sequence in *inputenc* encoding. Override to
        process the bytes in some other way (for example, for token
        translation).
        """
        if not isinstance(unicode_, basestring):
            raise TypeError(
                "expected unicode for encode input, but got {0} instead"
                .format(unicode_.__class__.__name__))
        # convert character by character
        for pos, c in enumerate(unicode_):
            # attempt input encoding first
            # if this succeeds, then we don't need a latex representation
            try:
                bytes_ = c.encode(self.inputenc, 'strict')
            except UnicodeEncodeError:
                pass
            else:
                space, bytes_ = self.get_space_bytes(bytes_)
                self.state = 'M'
                if space:
                    yield space
                yield bytes_
                continue
            # inputenc failed; let's try the latex equivalents
            # of common unicode characters
            try:
                bytes_, tokens = self.table.latex_map[c]
            except KeyError:
                # translation failed
                if errors == 'strict':
                    raise UnicodeEncodeError(
                        "latex", # codec
                        unicode_, # problematic input
                        pos, pos + 1, # location of problematic character
                        "don't know how to translate {1} ({0}) into latex"
                        .format(c, repr(c)))
                elif errors == 'ignore':
                    pass
                elif errors == 'replace':
                    # use the \\char command
                    # this assumes
                    # \usepackage[T1]{fontenc}
                    # \usepackage[utf8]{inputenc}
                    yield b'{\\char'
                    yield str(ord(c)).encode("ascii")
                    yield b'}'
                    self.state = 'M'
                else:
                    raise ValueError(
                        "latex codec does not support {0} errors"
                        .format(errors))
            else:
                # translation succeeded
                space, bytes_ = self.get_space_bytes(bytes_)
                # update state
                if tokens[-1].name == 'control_word':
                    # we're eating spaces
                    self.state = 'S'
                else:
                    self.state = 'M'
                if space:
                    yield space
                yield bytes_

class LatexIncrementalDecoder(latex_lexer.LatexIncrementalDecoder):
    """Translating incremental decoder for latex."""

    table = _LATEX_UNICODE_TABLE
    """Translation table."""

    def __init__(self, errors='strict'):
        latex_lexer.LatexIncrementalDecoder.__init__(self)
        self.max_length = 0

    def reset(self):
        latex_lexer.LatexIncrementalDecoder.reset(self)
        self.token_buffer = []

    # python codecs API does not support multibuffer incremental decoders

    def getstate(self):
        raise NotImplementedError

    def setstate(self, state):
        raise NotImplementedError

    def get_unicode_tokens(self, bytes_, final=False):
        for token in self.get_tokens(bytes_, final=final):
            # at this point, token_buffer does not match anything
            self.token_buffer.append(token)
            # new token appended at the end, see if we have a match now
            # note: match is only possible at the *end* of the buffer
            # because all other positions have already been checked in
            # earlier iterations
            for i in xrange(1, len(self.token_buffer) + 1):
                last_tokens = tuple(self.token_buffer[-i:]) # last i tokens
                try:
                    unicode_text = self.table.unicode_map[last_tokens]
                except KeyError:
                    # no match: continue
                    continue
                else:
                    # match!! flush buffer, and translate last bit
                    for token in self.token_buffer[:-i]: # exclude last i tokens
                        yield token.decode(self.inputenc)
                    yield unicode_text
                    self.token_buffer = []
                    break
            # flush tokens that can no longer match
            while len(self.token_buffer) >= self.table.max_length:
                yield self.token_buffer.pop(0).decode(self.inputenc)
        # also flush the buffer at the end
        if final:
            for token in self.token_buffer:
                yield token.decode(self.inputenc)
            self.token_buffer = []

class LatexCodec(codecs.Codec):
    IncrementalEncoder = None
    IncrementalDecoder = None

    def encode(self, unicode_, errors='strict'):
        """Convert unicode string to latex bytes."""
        return (
            self.IncrementalEncoder(errors=errors).encode(unicode_, final=True),
            len(unicode_),
            )

    def decode(self, bytes_, errors='strict'):
        """Convert latex bytes to unicode string."""
        return (
            self.IncrementalDecoder(errors=errors).decode(bytes_, final=True),
            len(bytes_),
            )

def find_latex(encoding):
    # check if requested codec info is for latex encoding
    if not encoding.startswith('latex'):
        return None
    # set up all classes with correct latex input encoding
    inputenc_ = encoding[6:] if encoding.startswith('latex+') else 'ascii'
    class IncrementalEncoder_(LatexIncrementalEncoder):
        inputenc = inputenc_
    class IncrementalDecoder_(LatexIncrementalDecoder):
        inputenc = inputenc_
    class Codec(LatexCodec):
        IncrementalEncoder = IncrementalEncoder_
        IncrementalDecoder = IncrementalDecoder_
    class StreamWriter(Codec, codecs.StreamWriter):
        pass
    class StreamReader(Codec, codecs.StreamReader):
        pass
    return codecs.CodecInfo(
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder_,
        incrementaldecoder=IncrementalDecoder_,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
        )

codecs.register(find_latex)
