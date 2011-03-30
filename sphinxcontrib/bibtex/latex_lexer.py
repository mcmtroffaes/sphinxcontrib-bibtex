"""
    Simple Tex Lexer
    ~~~~~~~~~~~~~~~~~~
"""

import re

class Token:
    """Stores information about a matched token."""

    def __init__(self, name=None, text=None):
        self.name = name if name is not None else 'unknown'
        self.text = text if text is not None else b''

    def __nonzero__(self):
        return bool(self.text)

class TexLexer:
    """A very simple incremental lexer for tex/latex code. Roughly
    follows the state machine descriped in Tex By Topic, Chapter 2.

    The generated tokens satisfy:

    * no newline characters: paragraphs are separated by '\\par'
    * spaces following control tokens are compressed
    """
    tokens = [
        # comment: for ease, and for speed, we handle it as a token
        ('comment', br'%.*?\n'),
        # control tokens
        # in latex, some control tokens skip following whitespace ('control')
        # others do not ('controlx')
        # XXX TBT says no control symbols skip whitespace (except '\ ')
        # XXX but tests reveal otherwise?
        ('control', br'[\\]([a-zA-Z]+|[~' + ur"'" + ur'"` =^!])'),
        ('controlx', br'[\\][^a-zA-Z]'),
        # parameter tokens
        ('parameter', br'\#[0-9]'),
        # any remaining characters; for ease we also handle space and
        # newline as tokens
        ('space', br' '),
        ('newline', br'\n'),
        ('mathshift', br'[$]'),
        ('chars', br'([^ %#$\n\\])+'),
        # trailing garbage which we cannot decode otherwise
        # (such as a lone '\' at the end of a buffer)
        # is never emitted, but used internally by the buffer
        ('unknown', br'.'),
        ]

    def __init__(self):
        """Initialize regular expression string."""
        # three possible states:
        # newline (N), skipping spaces (S), and middle of line (M)
        self.state = 'N'
        # inline math mode?
        self.inline_math = False
        # buffer for storing last (possibly incomplete) token
        self.buffer_ = Token()
        # regular expression used for matching
        self.regexp = re.compile(
            b"|".join(
                b"(?P<%s>%s)" % (name, regexp)
                for name, regexp in self.tokens),
            re.DOTALL)

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
        """Flush the raw token buffer."""
        if self.buffer_:
            if self.buffer_.name == 'unknown':
                raise AssertionError("unknown token: lexer bug?")
            yield self.buffer_
            self.buffer_ = Token()

    def get_tokens(self, bytes_, final=False):
        """Yield tokens while maintaining a state. Also skip
        whitespace after control words and (some) control symbols.
        Replaces newlines by spaces and \\par commands depending on
        the context.
        """
        for token in self.get_raw_tokens(bytes_, final=final):
            if token.name == 'newline':
                if self.state == 'N':
                    # if state was 'N', generate new paragraph
                    yield Token('control', '\\par')
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
            elif token.name == 'control':
                # go to space skip mode
                self.state = 'S'
                yield token
            elif token.name == 'controlx':
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
            else:
                raise AssertionError(
                    "unknown token name '%s'" % token.name)
