"""Tests for the tex lexer."""

import nose.tools
from unittest import TestCase

from sphinxcontrib.bibtex.latex_lexer import (
    LatexLexer, LatexIncrementalDecoder, LatexIncrementalEncoder, Token)


def test_token_create():
    t = Token()
    nose.tools.assert_equal(t.name, 'unknown')
    nose.tools.assert_equal(t.text, b'')


def test_token_create_with_args():
    t = Token('hello', b'world')
    nose.tools.assert_equal(t.name, 'hello')
    nose.tools.assert_equal(t.text, b'world')


@nose.tools.raises(AttributeError)
def test_token_assign_name():
    t = Token()
    t.name = 'test'


@nose.tools.raises(AttributeError)
def test_token_assign_text():
    t = Token()
    t.text = 'test'


@nose.tools.raises(AttributeError)
def test_token_assign_other():
    t = Token()
    t.blabla = 'test'


class BaseLatexLexerTest(TestCase):

    errors = 'strict'

    def setUp(self):
        self.lexer = LatexLexer(errors=self.errors)

    def lex_it(self, latex_code, latex_tokens, final=False):
        tokens = self.lexer.get_raw_tokens(latex_code, final=final)
        self.assertEqual(
            list(token.text for token in tokens),
            latex_tokens)

    def tearDown(self):
        del self.lexer


class LatexLexerTest(BaseLatexLexerTest):

    def test_null(self):
        self.lex_it(b'', [], final=True)

    def test_hello(self):
        self.lex_it(
            b'hello!  [#1] This \\is\\   \\^ a \ntest.\n'
            b'    \nHey.\n\n\# x \#x',
            br'h|e|l|l|o|!| | |[|#1|]| |T|h|i|s| |\is|\ | | |\^| |a| '
            b'|\n|t|e|s|t|.|\n| | | | |\n|H|e|y|.|\n|\n'
            br'|\#| |x| |\#|x'.split(b'|'),
            final=True
        )

    def test_comment(self):
        self.lex_it(
            b'test% some comment\ntest',
            b't|e|s|t|% some comment\n|t|e|s|t'.split(b'|'),
            final=True
        )

    def test_comment_newline(self):
        self.lex_it(
            b'test% some comment\n\ntest',
            b't|e|s|t|% some comment\n|\n|t|e|s|t'.split(b'|'),
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
            b'\\hello| | | |\\world| | | '.split(b'|'),
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
            b'\\#| | | | |\\&| | | '.split(b'|'),
            final=True
        )

    def test_buffer(self):
        self.lex_it(
            b'hi\\t',
            b'h|i'.split(b'|'),
        )
        self.lex_it(
            b'here',
            [b'\\there'],
            final=True,
        )

    def test_state(self):
        self.lex_it(
            b'hi\\t',
            b'h|i'.split(b'|'),
        )
        state = self.lexer.getstate()
        self.lexer.reset()
        self.lex_it(
            b'here',
            b'h|e|r|e'.split(b'|'),
            final=True,
        )
        self.lexer.setstate(state)
        self.lex_it(
            b'here',
            [b'\\there'],
            final=True,
        )

    @nose.tools.raises(NotImplementedError)
    def test_decode(self):
            self.lexer.decode(b'')

    def test_final_backslash(self):
        self.lex_it(
            b'notsogood\\',
            b'n|o|t|s|o|g|o|o|d|\\'.split(b'|'),
            final=True
        )

    def test_final_comment(self):
        self.lex_it(
            b'hello%',
            b'h|e|l|l|o|%'.split(b'|'),
            final=True
        )

    def test_hash(self):
        self.lex_it(b'#', [b'#'], final=True)


class BaseTexLexerTest(TestCase):

    """Tex lexer fixture."""

    errors = 'strict'

    def setUp(self):
        self.lexer = LatexIncrementalDecoder(self.errors)

    def lex_it(self, latex_code, latex_tokens, final=False):
        tokens = self.lexer.get_tokens(latex_code, final=final)
        self.assertEqual(
            list(token.text for token in tokens),
            latex_tokens)

    def tearDown(self):
        del self.lexer


class TexLexerTest(BaseTexLexerTest):

    def test_null(self):
        self.lex_it(b'', [], final=True)

    def test_hello(self):
        self.lex_it(
            b'hello!  [#1] This \\is\\   \\^ a \ntest.\n'
            b'    \nHey.\n\n\# x \#x',
            br'h|e|l|l|o|!| |[|#1|]| |T|h|i|s| |\is|\ |\^|a| '
            br'|t|e|s|t|.| |\par|H|e|y|.| '
            br'|\par|\#| |x| |\#|x'.split(b'|'),
            final=True
        )

    def test_comment(self):
        self.lex_it(
            b'test% some comment\ntest',
            b't|e|s|t|t|e|s|t'.split(b'|'),
            final=True
        )

    def test_comment_newline(self):
        self.lex_it(
            b'test% some comment\n\ntest',
            b't|e|s|t|\\par|t|e|s|t'.split(b'|'),
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
            b'h|i'.split(b'|'),
        )
        self.lex_it(
            b'here',
            [b'\\there'],
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

    def test_state_middle(self):
        self.lex_it(
            b'hi\\t',
            b'h|i'.split(b'|'),
        )
        state = self.lexer.getstate()
        self.assertEqual(self.lexer.state, 'M')
        self.assertEqual(self.lexer.raw_buffer.name, 'control_word')
        self.assertEqual(self.lexer.raw_buffer.text, b'\\t')
        self.lexer.reset()
        self.assertEqual(self.lexer.state, 'N')
        self.assertEqual(self.lexer.raw_buffer.name, 'unknown')
        self.assertEqual(self.lexer.raw_buffer.text, b'')
        self.lex_it(
            b'here',
            b'h|e|r|e'.split(b'|'),
            final=True,
        )
        self.lexer.setstate(state)
        self.assertEqual(self.lexer.state, 'M')
        self.assertEqual(self.lexer.raw_buffer.name, 'control_word')
        self.assertEqual(self.lexer.raw_buffer.text, b'\\t')
        self.lex_it(
            b'here',
            [b'\\there'],
            final=True,
        )

    def test_state_inline_math(self):
        self.lex_it(
            b'hi$t',
            b'h|i|$'.split(b'|'),
        )
        assert self.lexer.inline_math
        self.lex_it(
            b'here$',
            b't|h|e|r|e|$'.split(b'|'),
            final=True,
        )
        assert not self.lexer.inline_math

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

    def test_hash(self):
        self.lex_it(b'#', [b'#'], final=True)


class TexLexerReplaceTest(BaseTexLexerTest):

    errors = 'replace'

    def test_errors_replace(self):
        self.lex_it(
            b'hello%',
            b'h|e|l|l|o|?'.split(b'|'),
            final=True
        )


class TexLexerIgnoreTest(BaseTexLexerTest):

    errors = 'ignore'

    def test_errors_ignore(self):
        self.lex_it(
            b'hello%',
            b'h|e|l|l|o'.split(b'|'),
            final=True
        )


class TexLexerInvalidErrorTest(BaseTexLexerTest):

    errors = '**baderror**'

    @nose.tools.raises(NotImplementedError)
    def test_errors_invalid(self):
        self.lex_it(
            b'hello%',
            b'h|e|l|l|o'.split(b'|'),
            final=True
        )


def invalid_token_test():
    lexer = LatexIncrementalDecoder()
    # piggyback an implementation which results in invalid tokens
    lexer.get_raw_tokens = lambda bytes_, final: [Token('**invalid**', bytes_)]
    nose.tools.assert_raises(AssertionError, lambda: lexer.decode(b'hello'))


def invalid_state_test_1():
    lexer = LatexIncrementalDecoder()
    # piggyback invalid state
    lexer.state = '**invalid**'
    nose.tools.assert_raises(AssertionError, lambda: lexer.decode(b'\n\n\n'))


def invalid_state_test_2():
    lexer = LatexIncrementalDecoder()
    # piggyback invalid state
    lexer.state = '**invalid**'
    nose.tools.assert_raises(AssertionError, lambda: lexer.decode(b'   '))


class LatexIncrementalEncoderTest(TestCase):

    """Encoder test fixture."""

    errors = 'strict'

    def setUp(self):
        self.encoder = LatexIncrementalEncoder(self.errors)

    def encode(self, latex_code, latex_bytes, final=False):
        result = self.encoder.encode(latex_code, final=final)
        self.assertEqual(result, latex_bytes)

    def tearDown(self):
        del self.encoder

    @nose.tools.raises(TypeError)
    def test_invalid_type(self):
        self.encoder.encode(object())

    @nose.tools.raises(ValueError)
    def test_invalid_code(self):
        # default encoding is ascii, \u00ff is not ascii translatable
        self.encoder.encode(u"\u00ff")

    def test_hello(self):
        self.encode(u'hello', b'hello')
