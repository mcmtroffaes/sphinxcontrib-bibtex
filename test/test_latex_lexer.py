"""Tests for the tex lexer."""

from unittest import TestCase

from sphinxcontrib.bibtex.latex_lexer import TexLexer

class TexLexerTest(TestCase):
    """Tex lexer fixture."""
    def setUp(self):
        self.lexer = TexLexer()

    def test_hello(self):
        self.assertEqual(
            list(self.lexer.get_tokens(
                b'hello!  [#1] This \\is\\   \\^ a \ntest.\n'
                b'    \nHey.\n\n\# x \#x')),
            br'h|e|l|l|o|!| |[|#1|]| |T|h|i|s| |\is|\ |\^|a| '
            br'|t|e|s|t|.| |\par|H|e|y|.| '
            br'|\par|\#| |x| |\#|x'.split(b'|')
            )
