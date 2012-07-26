# -*- coding: utf-8 -*-
"""
    Simple incremental latex lexer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import codecs
import collections
import re

class Token(collections.namedtuple("Token", "name text")):
    """Stores information about a matched token."""
    __slots__ = () # efficiency

    def __new__(cls, name=None, text=None):
        return tuple.__new__(
            cls,
            (name if name is not None else 'unknown',
             text if text is not None else b''))

    def __nonzero__(self):
        return bool(self.text)

    def __len__(self):
        return len(self.text)

    def decode(self, encoding):
        if self.name == 'control_word':
            return self.text.decode(encoding) + u' '
        else:
            return self.text.decode(encoding)

# implementation note: we derive from IncrementalDecoder because this
# class serves excellently as a base class for incremental decoders,
# but of course we don't decode yet until later
class LatexLexer(codecs.IncrementalDecoder):
    """A very simple lexer for tex/latex code."""

    # implementation note: every token **must** be decodable by inputenc
    tokens = [
        # comment: for ease, and for speed, we handle it as a token
        ('comment', br'%.*?\n'),
        # control tokens
        # in latex, some control tokens skip following whitespace
        # ('control-word' and 'control-symbol')
        # others do not ('control-symbol-x')
        # XXX TBT says no control symbols skip whitespace (except '\ ')
        # XXX but tests reveal otherwise?
        ('control_word', br'[\\][a-zA-Z]+'),
        ('control_symbol', br'[\\][~' br"'" br'"` =^!]'),
        ('control_symbol_x', br'[\\][^a-zA-Z]'), # TODO should only match ascii
        # parameter tokens
        # also support a lone hash so we can lex things like b'#a'
        ('parameter', br'\#[0-9]|\#'),
        # any remaining characters; for ease we also handle space and
        # newline as tokens
        ('space', br' '),
        ('newline', br'\n'),
        ('mathshift', br'[$]'),
        # note: some chars joined together to make it easier to detect
        # symbols that have a special function (i.e. --, ---, etc.)
        ('chars',
         br'---|--|-|[`][`]'
         br"|['][']"
         br'|[?][`]|[!][`]'
         # separate chars because brackets are optional
         # e.g. fran\\c cais = fran\\c{c}ais in latex
         # so only way to detect \\c acting on c only is this way
         br'|[0-9a-zA-Z{}]'
         # we have to join everything else together to support
         # multibyte encodings: every token must be decodable!!
         # this means for instance that \\c öké is NOT equivalent to
         # \\c{ö}ké
         br'|[^ %#$\n\\]+'),
        # trailing garbage which we cannot decode otherwise
        # (such as a lone '\' at the end of a buffer)
        # is never emitted, but used internally by the buffer
        ('unknown', br'.'),
        ]

    def __init__(self, errors='strict'):
        """Initialize the codec."""
        self.errors = errors
        # regular expression used for matching
        self.regexp = re.compile(
            b"|".join(
                b"(?P<" + name.encode() + b">" + regexp + b")"
                for name, regexp in self.tokens),
            re.DOTALL)
        # reset state
        self.reset()

    def reset(self):
        """Reset state (also called by __init__ to initialize the
        state).
        """
        # buffer for storing last (possibly incomplete) token
        self.raw_buffer = Token()

    def getstate(self):
        return (self.raw_buffer.text, 0)

    def setstate(self, state):
        self.raw_buffer = Token('unknown', state[0])

    def get_raw_tokens(self, bytes_, final=False):
        """Yield tokens without any further processing. Tokens are one of:

        - ``\\<word>``: a control word (i.e. a command)
        - ``\\<symbol>``: a control symbol (i.e. \\^ etc.)
        - ``#<n>``: a parameter
        - a series of byte characters
        """
        if not isinstance(bytes_, bytes):
            raise TypeError(
                'expected bytes but got %s'
                % bytes_.__class__.__name__)
        if self.raw_buffer:
            bytes_ = self.raw_buffer.text + bytes_
        self.raw_buffer = Token()
        for match in self.regexp.finditer(bytes_):
            for name, regexp in self.tokens:
                text = match.group(name)
                if text is not None:
                    # yield the buffer token(s)
                    for token in self.flush_raw_tokens():
                        yield token
                    # fill buffer with next token
                    self.raw_buffer = Token(name, text)
                    break
            else:
                # should not happen
                raise AssertionError("lexer failed on '%s'" % bytes_)
        if final:
            for token in self.flush_raw_tokens():
                yield token

    def flush_raw_tokens(self):
        """Flush the raw token buffer."""
        if self.raw_buffer:
            yield self.raw_buffer
            self.raw_buffer = Token()

class LatexIncrementalLexer(LatexLexer):
    """A very simple incremental lexer for tex/latex code. Roughly
    follows the state machine described in Tex By Topic, Chapter 2.

    The generated tokens satisfy:

    * no newline characters: paragraphs are separated by '\\par'
    * spaces following control tokens are compressed
    """

    def reset(self):
        """Reset state (also called by __init__ to initialize the
        state).
        """
        LatexLexer.reset(self)
        # three possible states:
        # newline (N), skipping spaces (S), and middle of line (M)
        self.state = 'N'
        # inline math mode?
        self.inline_math = False

    def getstate(self):
        # state 'M' is most common, so let that be zero
        return (
            self.raw_buffer,
            {'M': 0, 'N': 1, 'S': 2}[self.state]
            | (4 if self.inline_math else 0)
            )

    def setstate(self, state):
        self.raw_buffer = state[0]
        self.state = {0: 'M', 1: 'N', 2: 'S'}[state[1] & 3]
        self.inline_math = bool(state[1] & 4)

    def get_tokens(self, bytes_, final=False):
        """Yield tokens while maintaining a state. Also skip
        whitespace after control words and (some) control symbols.
        Replaces newlines by spaces and \\par commands depending on
        the context.
        """
        # current position relative to the start of bytes_ in the sequence
        # of bytes that have been decoded
        pos = -len(self.raw_buffer)
        for token in self.get_raw_tokens(bytes_, final=final):
            pos = pos + len(token)
            assert pos >= 0 # first token includes at least self.raw_buffer
            if token.name == 'newline':
                if self.state == 'N':
                    # if state was 'N', generate new paragraph
                    yield Token('control_word', b'\\par')
                elif self.state == 'S':
                    # switch to 'N' state, do not generate a space
                    self.state = 'N'
                elif self.state == 'M':
                    # switch to 'N' state, generate a space
                    self.state = 'N'
                    yield Token('space', b' ')
                else:
                    raise AssertionError(
                        "unknown tex state '%s'" % self.state)
            elif token.name == 'space':
                if self.state == 'N':
                    # remain in 'N' state, no space token generated
                    pass
                elif self.state == 'S':
                    # remain in 'S' state, no space token generated
                    pass
                elif self.state == 'M':
                    # in M mode, generate the space,
                    # but switch to space skip mode
                    self.state = 'S'
                    yield token
                else:
                    raise AssertionError(
                        "unknown state %s" % repr(self.state))
            elif token.name == 'char':
                self.state = 'M'
                yield token
            elif token.name == 'mathshift':
                self.inline_math = not self.inline_math
                yield token
            elif token.name == 'parameter':
                self.state = 'M'
                yield token
            elif token.name == 'control_word':
                # go to space skip mode
                self.state = 'S'
                yield token
            elif token.name == 'control_symbol':
                # go to space skip mode
                self.state = 'S'
                yield token
            elif token.name == 'control_symbol_x':
                # don't skip following space, so go to M mode
                self.state = 'M'
                yield token
            elif token.name == 'comment':
                # go to newline mode, no token is generated
                # note: comment includes the newline
                self.state = 'N'
            elif token.name == 'chars':
                self.state = 'M'
                yield token
            elif token.name == 'unknown':
                if self.errors == 'strict':
                    # current position within bytes_
                    # this is the position right after the unknown token
                    raise UnicodeDecodeError(
                        "latex", # codec
                        bytes_, # problematic input
                        pos - len(token), # start of problematic token
                        pos, # end of it
                        "unknown token %s" % repr(token.text))
                elif self.errors == 'ignore':
                    # do nothing
                    pass
                elif self.errors == 'replace':
                    yield Token('chars', b'?' * len(token))
                else:
                    raise NotImplementedError(
                        "error mode %s not supported" % repr(self.errors))

class LatexIncrementalDecoder(LatexIncrementalLexer):
    """Simple incremental decoder. Transforms lexed latex tokens into
    unicode.

    To customize decoding, subclass and override
    :meth:`get_unicode_tokens`.
    """

    inputenc = "ascii"
    """Input encoding. **Must** extend ascii."""

    def get_unicode_tokens(self, bytes_, final=False):
        """:meth:`decode` calls this function to produce the final
        sequence of unicode strings. This implementation simply
        decodes every sequence in *inputenc* encoding. Override to
        process the tokens in some other way (for example, for token
        translation).
        """
        for token in self.get_tokens(bytes_, final=final):
            yield token.decode(self.inputenc)

    def decode(self, bytes_, final=False):
        try:
            return u''.join(self.get_unicode_tokens(bytes_, final=final))
        except UnicodeDecodeError, e:
            # API requires that the encode method raises a ValueError
            # in this case
            raise ValueError(e)

class LatexIncrementalEncoder(codecs.IncrementalEncoder):
    """Simple incremental encoder for latex."""

    inputenc = "ascii"
    """Input encoding. **Must** extend ascii."""

    def get_latex_bytes(self, unicode_):
        """:meth:`encode` calls this function to produce the final
        sequence of latex bytes. This implementation simply
        encodes every sequence in *inputenc* encoding. Override to
        process the unicode in some other way (for example, for character
        translation).
        """
        if not isinstance(unicode_, basestring):
            raise TypeError(
                "expected unicode for encode input, but got {0} instead"
                .format(unicode_.__class__.__name__))
        for c in unicode_:
            yield c.encode(inputenc, self.errors)

    def encode(self, unicode_, final=False):
        """Encode unicode string into a latex byte sequence."""
        try:
            return b''.join(self.get_latex_bytes(unicode_, final=final))
        except UnicodeDecodeError, e:
            # API requires that the encode method raises a ValueError
            # in this case
            raise ValueError(e)
