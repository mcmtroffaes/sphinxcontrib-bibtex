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

class LatexIncrementalDecoder(codecs.IncrementalDecoder):
    """A very simple incremental lexer for tex/latex code. Roughly
    follows the state machine descriped in Tex By Topic, Chapter 2.

    The generated tokens satisfy:

    * no newline characters: paragraphs are separated by '\\par'
    * spaces following control tokens are compressed

    The easiest way to customize decoding is to subclass and
    overriding :meth:`get_unicode_tokens`.
    """

    inputenc = "ascii"
    """Default input encoding. **Must** extend ascii."""

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
        ('parameter', br'\#[0-9]'),
        # any remaining characters; for ease we also handle space and
        # newline as tokens
        ('space', br' '),
        ('newline', br'\n'),
        ('mathshift', br'[$]'),
        # note: some chars joined together to make it easier to detect
        # symbols that have a special function (i.e. --, ---, etc.)
        ('chars',
         br'---|--|[`][`]'
         br"|['][']"
         br'|[?][`]|[!][`]'
         br'|[^ %#$\n\\]'),
        # trailing garbage which we cannot decode otherwise
        # (such as a lone '\' at the end of a buffer)
        # is never emitted, but used internally by the buffer
        ('unknown', br'.'),
        ]

    def __init__(self, errors='strict'):
        """Initialize the codec."""
        codecs.IncrementalDecoder.__init__(self, errors)
        # regular expression used for matching
        self.regexp = re.compile(
            b"|".join(
                b"(?P<%s>%s)" % (name, regexp)
                for name, regexp in self.tokens),
            re.DOTALL)
        # reset state
        self.reset()

    def reset(self):
        """Reset state."""
        # three possible states:
        # newline (N), skipping spaces (S), and middle of line (M)
        self.state = 'N'
        # inline math mode?
        self.inline_math = False
        # buffer for storing last (possibly incomplete) token
        self.buffer_ = Token()
        # keeps track of how many bytes have been consumed in total
        self.consumed = 0

    def get_raw_tokens(self, bytes_, final=False):
        """Yield tokens without any further processing. Tokens are one of:

        - ``\\<word>``: a control word (i.e. a command)
        - ``\\<symbol>``: a control symbol (i.e. \\^ etc.)
        - ``#<n>``: a parameter
        - a series of byte characters
        """
        if self.buffer_:
            bytes_ = self.buffer_.text + bytes_
        self.buffer_ = Token()
        for match in self.regexp.finditer(bytes_):
            for name, regexp in self.tokens:
                text = match.group(name)
                if text is not None:
                    # yield the buffer token(s)
                    for token in self.flush_raw_tokens():
                        yield token
                    # fill buffer with next token
                    self.buffer_ = Token(name, text)
                    break
            else:
                # should not happen
                raise AssertionError("lexer failed on '%s'" % bytes_)
        if final:
            for token in self.flush_raw_tokens():
                yield token

    def flush_raw_tokens(self):
        """Flush the raw token buffer, and update number of consumed
        bytes.
        """
        if self.buffer_:
            self.consumed += len(self.buffer_)
            yield self.buffer_
            self.buffer_ = Token()

    def get_tokens(self, bytes_, final=False):
        """Yield tokens while maintaining a state. Also skip
        whitespace after control words and (some) control symbols.
        Replaces newlines by spaces and \\par commands depending on
        the context.
        """
        # mark the start of bytes_ in the sequence of all decoded bytes
        # so far (we need this when reporting errors)
        start = self.consumed + len(self.buffer_)
        for token in self.get_raw_tokens(bytes_, final=final):
            if token.name == 'newline':
                if self.state == 'N':
                    # if state was 'N', generate new paragraph
                    yield Token('control_word', '\\par')
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
                        "unknown tex state '%s'" % self.state)
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
                    pos = self.consumed - start
                    raise UnicodeDecodeError(
                        "latex", # codec
                        bytes_, # problematic input
                        pos - len(token), # start of problematic token
                        pos, # end of it
                        "unknown token %s" % repr(self.buffer_.text))
                elif self.errors == 'ignore':
                    # do nothing
                    pass
                elif self.errors == 'replace':
                    yield Token('chars', b'?' * len(token))
                else:
                    raise NotImplementedError(
                        "error mode %s not supported" % repr(self.errors))

    def get_unicode_tokens(self, bytes_, final=False):
        """:meth:`decode` calls this function to produce the final
        sequence of unicode strings. This implementation simply
        decodes every sequence in *inputenc* encoding. Override to
        process the tokens in some other way (for example, for token
        translation).
        """
        return (token.decode(self.inputenc)
                for token in self.get_tokens(bytes_, final=final))

    def decode(self, bytes_, final=False):
        try:
            return u''.join(self.get_unicode_tokens(bytes_, final=final))
        except UnicodeDecodeError, e:
            # API requires that the encode method raises a ValueError
            # in this case
            raise ValueError(e)
