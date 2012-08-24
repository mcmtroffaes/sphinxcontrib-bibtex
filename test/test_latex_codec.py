# -*- coding: utf-8 -*-
"""Tests for the latex codec."""

from __future__ import print_function

import codecs
import sys
if sys.version_info >= (3, 0):
    from io import BytesIO
else:
    from cStringIO import StringIO as BytesIO
from nose.exc import SkipTest
from unittest import TestCase

import sphinxcontrib.bibtex.latex_codec # registers automatically

def split_input(input_):
    """Helper function for testing the incremental encoder and decoder."""
    if isinstance(input_, unicode):
        sep = u" "
    elif isinstance(input_, bytes):
        sep = b" "
    else:
        raise TypeError("expected unicode or bytes input")
    part1, part2, part3 = input_.partition(sep)
    if part3:
        yield part1, False
        yield part2, False
        for part, final in split_input(part3):
            yield part, final
    else:
        # last part
        yield part1, True

class TestDecoder(TestCase):
    """Stateless decoder tests."""
    maxDiff = None

    def decode(self, text_utf8, text_latex, inputenc=None):
        """Main test function."""
        encoding = 'latex+' + inputenc if inputenc else 'latex'
        decoded, n = codecs.getdecoder(encoding)(text_latex)
        self.assertEqual((decoded, n), (text_utf8, len(text_latex)))

    def test_null(self):
        self.decode(u'', b'')

    def test_maelstrom(self):
        self.decode(u"mælström", br'm\ae lstr\"om')

    def test_maelstrom_latin1(self):
        self.decode(u"mælström", b'm\\ae lstr\xf6m', 'latin1')

    def test_laren(self):
        self.decode(
            u"©\\ låren av björn",
            br'\copyright\ l\aa ren av bj\"orn')

    def test_laren_brackets(self):
        self.decode(
            u"©\\ l{å}ren av bj{ö}rn",
            br'\copyright\ l{\aa}ren av bj{\"o}rn')

    def test_laren_latin1(self):
        self.decode(
            u"©\\ låren av björn",
            b'\\copyright\\ l\xe5ren av bj\xf6rn',
            'latin1')

    def test_droitcivil(self):
        self.decode(
            u"Même s'il a fait l'objet d'adaptations suite à l'évolution, "
            u"la transformation sociale, économique et politique du pays, "
            u"le code civil fran{ç}ais est aujourd'hui encore le texte fondateur "
            u"du droit civil français mais aussi du droit civil belge ainsi que "
            u"de plusieurs autres droits civils.",
            b"M\\^eme s'il a fait l'objet d'adaptations suite "
            b"\\`a l'\\'evolution, \nla transformation sociale, "
            b"\\'economique et politique du pays, \nle code civil "
            b"fran\\c{c}ais est aujourd'hui encore le texte fondateur \n"
            b"du droit civil fran\\c cais mais aussi du droit civil "
            b"belge ainsi que \nde plusieurs autres droits civils.",
            )

    def test_oeuf(self):
        self.decode(
            u"D'un point de vue diététique, l'œuf apaise la faim.",
            br"D'un point de vue di\'et\'etique, l'\oe uf apaise la faim.",
            )

    def test_oeuf_latin1(self):
        self.decode(
            u"D'un point de vue diététique, l'œuf apaise la faim.",
            b"D'un point de vue di\xe9t\xe9tique, l'\\oe uf apaise la faim.",
            'latin1'
            )

    def test_alpha(self):
        self.decode(u"α", b"$\\alpha$")

    def test_maelstrom_multibyte_encoding(self):
        self.decode(u"\\c öké", b'\\c \xc3\xb6k\xc3\xa9', 'utf8')

    def test_serafin(self):
        self.decode(u"Seraf{\xed}n", b"Seraf{\\'i}n")

    def test_astrom(self):
        self.decode(u"{\xc5}str{\xf6}m", b'{\\AA}str{\\"o}m')

class TestStreamDecoder(TestDecoder):
    """Stream decoder tests."""

    def decode(self, text_utf8, text_latex, inputenc=None):
        encoding = 'latex+' + inputenc if inputenc else 'latex'
        stream = BytesIO(text_latex)
        reader = codecs.getreader(encoding)(stream)
        self.assertEqual(text_utf8, reader.read())

class TestIncrementalDecoder(TestDecoder):
    """Incremental decoder tests."""

    def decode(self, text_utf8, text_latex, inputenc=None):
        encoding = 'latex+' + inputenc if inputenc else 'latex'
        decoder = codecs.getincrementaldecoder(encoding)()
        decoded_parts = (
            decoder.decode(text_latex_part, final)
            for text_latex_part, final in split_input(text_latex))
        self.assertEqual(text_utf8, u''.join(decoded_parts))

class TestEncoder(TestCase):
    """Stateless encoder tests."""

    def encode(self, text_utf8, text_latex, inputenc=None):
        """Main test function."""
        encoding = 'latex+' + inputenc if inputenc else 'latex'
        encoded, n = codecs.getencoder(encoding)(text_utf8)
        self.assertEqual((encoded, n), (text_latex, len(text_utf8)))

    def test_null(self):
        self.encode(u'', b'')

    def test_maelstrom(self):
        self.encode(u"mælström", br'm\ae lstr\"om')

    def test_maelstrom_latin1(self):
        self.encode(u"mælström", b'm\xe6lstr\xf6m', 'latin1')

    def test_laren(self):
        self.encode(
            u"© låren av björn",
            br'\copyright\ l\aa ren av bj\"orn')

    def test_laren_latin1(self):
        self.encode(
            u"© låren av björn",
            b'\xa9 l\xe5ren av bj\xf6rn',
            'latin1')

    def test_droitcivil(self):
        self.encode(
            u"Même s'il a fait l'objet d'adaptations suite à l'évolution, \n"
            u"la transformation sociale, économique et politique du pays, \n"
            u"le code civil fran{ç}ais est aujourd'hui encore le texte fondateur \n"
            u"du droit civil français mais aussi du droit civil belge ainsi que \n"
            u"de plusieurs autres droits civils.",
            b"M\\^eme s'il a fait l'objet d'adaptations suite "
            b"\\`a l'\\'evolution, \nla transformation sociale, "
            b"\\'economique et politique du pays, \nle code civil "
            b"fran{\\c c}ais est aujourd'hui encore le texte fondateur \n"
            b"du droit civil fran\\c cais mais aussi du droit civil "
            b"belge ainsi que \nde plusieurs autres droits civils.",
            )

    def test_oeuf(self):
        self.encode(
            u"D'un point de vue diététique, l'œuf apaise la faim.",
            br"D'un point de vue di\'et\'etique, l'\oe uf apaise la faim.",
            )

    def test_oeuf_latin1(self):
        self.encode(
            u"D'un point de vue diététique, l'œuf apaise la faim.",
            b"D'un point de vue di\xe9t\xe9tique, l'\\oe uf apaise la faim.",
            'latin1'
            )

    def test_alpha(self):
        self.encode(u"α", b"$\\alpha$")

    def test_serafin(self):
        self.encode(u"Seraf{\xed}n", b"Seraf{\\'\\i }n")

class TestStreamEncoder(TestEncoder):
    """Stream encoder tests."""

    def encode(self, text_utf8, text_latex, inputenc=None):
        encoding = 'latex+' + inputenc if inputenc else 'latex'
        stream = BytesIO()
        writer = codecs.getwriter(encoding)(stream)
        writer.write(text_utf8)
        self.assertEqual(text_latex, stream.getvalue())

class TestIncrementalEncoder(TestEncoder):
    """Incremental encoder tests."""

    def encode(self, text_utf8, text_latex, inputenc=None):
        encoding = 'latex+' + inputenc if inputenc else 'latex'
        encoder = codecs.getincrementalencoder(encoding)()
        encoded_parts = (
            encoder.encode(text_utf8_part, final)
            for text_utf8_part, final in split_input(text_utf8))
        self.assertEqual(text_latex, b''.join(encoded_parts))
