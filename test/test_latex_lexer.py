"""Tests for the tex lexer."""

import nose.tools
from unittest import TestCase

from sphinxcontrib.bibtex.latex_lexer import LatexIncrementalDecoder

class BaseTexLexerTest(TestCase):
    """Tex lexer fixture."""

    errors = 'strict'

    def setUp(self):
        self.lexer = LatexIncrementalDecoder(self.errors)

    def lex_it(self, latex_code, latex_tokens, consumed=None, final=False):
        tokens = self.lexer.get_tokens(latex_code, final=final)
        self.assertEqual(
            list(token.text for token in tokens),
            latex_tokens)
        if consumed is None:
            consumed = len(latex_code)
        self.assertEqual(self.lexer.consumed, consumed)

    def tearDown(self):
        del self.lexer

class TexLexerTest(BaseTexLexerTest):

    def test_null(self):
        self.lex_it(b'', [], final=True)

    def test_hello(self):
        self.lex_it(
            b'hello!  [#1] This \\is\\   \\^ a \ntest.\n'
            b'    \nHey.\n\n\# x \#x',
            br'hello!| |[|#1|]| |This| |\is|\ |\^|a| '
            br'|test.| |\par|Hey.| '
            br'|\par|\#| |x| |\#|x'.split(b'|'),
            final=True
            )

    def test_comment(self):
        self.lex_it(
            b'test% some comment\ntest',
            b'test|test'.split(b'|'),
            final=True
            )

    def test_comment_newline(self):
        self.lex_it(
            b'test% some comment\n\ntest',
            b'test|\\par|test'.split(b'|'),
            final=True
            )

    def test_control(self):
        self.lex_it(
            b'\\hello\\world',
            b'\\hello|\\world'.split(b'|'),
            final=True
            )

    def test_control_whitespace(self):
        self.lex_it(
            b'\\hello   \\world   ',
            b'\\hello|\\world'.split(b'|'),
            final=True
            )

    def test_controlx(self):
        self.lex_it(
            b'\\#\\&',
            b'\\#|\\&'.split(b'|'),
            final=True
            )

    def test_controlx_whitespace(self):
        self.lex_it(
            b'\\#    \\&   ',
            b'\\#| |\\&| '.split(b'|'),
            final=True
            )

    def test_buffer(self):
        self.lex_it(
            b'hi\\t',
            [b'hi'],
            consumed=2,
            )
        self.lex_it(
            b'here',
            [b'\\there'],
            consumed=8,
            final=True,
            )

    def test_buffer_decode(self):
        self.assertEqual(
            self.lexer.decode(b'hello!  [#1] This \\i'),
            u'hello! [#1] This ',
            )
        self.assertEqual(
            self.lexer.decode(b's\\   \\^ a \ntest.\n'),
            u'\\is \\ \\^a test.',
            )
        self.assertEqual(
            self.lexer.decode(b'    \nHey.\n\n\# x \#x', final=True),
            u' \\par Hey. \\par \\# x \\#x',
            )

    # counterintuitive?
    @nose.tools.raises(UnicodeDecodeError)
    def test_final_backslash(self):
        self.lex_it(
            b'notsogood\\',
            [b'notsogood'],
            final=True
            )

    # counterintuitive?
    @nose.tools.raises(UnicodeDecodeError)
    def test_final_comment(self):
        self.lex_it(
            b'hello%',
            [b'hello'],
            final=True
            )

class TexLexerReplaceTest(BaseTexLexerTest):

    errors = 'replace'

    def test_errors_replace(self):
        self.lex_it(
            b'hello%',
            [b'hello', b'?'],
            final=True
            )
        
class TexLexerIgnoreTest(BaseTexLexerTest):

    errors = 'ignore'

    def test_errors_ignore(self):
        self.lex_it(
            b'hello%',
            [b'hello'],
            final=True
            )
        
