"""Tests for the tex lexer."""

from unittest import TestCase

from sphinxcontrib.bibtex.latex_lexer import TexLexer

class TexLexerTest(TestCase):
    """Tex lexer fixture."""
    def setUp(self):
        self.lexer = TexLexer()

    def lex_it(self, latex_code, latex_tokens):
        tokens = self.lexer.get_tokens(latex_code)
        self.assertEqual(
            list(token for name, token in tokens),
            latex_tokens)

    def test_null(self):
        self.lex_it(b'', [])

    def test_hello(self):
        self.lex_it(
            b'hello!  [#1] This \\is\\   \\^ a \ntest.\n'
            b'    \nHey.\n\n\# x \#x',
            br'h|e|l|l|o|!| |[|#1|]| |T|h|i|s| |\is|\ |\^|a| '
            br'|t|e|s|t|.| |\par|H|e|y|.| '
            br'|\par|\#| |x| |\#|x'.split(b'|')
            )

    def test_comment(self):
        self.lex_it(
            b'test% some comment\ntest',
            b't|e|s|t|t|e|s|t'.split(b'|')
            )

    def test_comment_newline(self):
        self.lex_it(
            b'test% some comment\n\ntest',
            b't|e|s|t|\\par|t|e|s|t'.split(b'|')
            )

    def test_control(self):
        self.lex_it(
            b'\\hello\\world',
            b'\\hello|\\world'.split(b'|')
            )

    def test_control_whitespace(self):
        self.lex_it(
            b'\\hello   \\world   ',
            b'\\hello|\\world'.split(b'|')
            )

    def test_controlx(self):
        self.lex_it(
            b'\\#\\&',
            b'\\#|\\&'.split(b'|')
            )

    def test_controlx_whitespace(self):
        self.lex_it(
            b'\\#    \\&   ',
            b'\\#| |\\&| '.split(b'|')
            )
