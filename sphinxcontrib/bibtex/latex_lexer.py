"""
    Simple Tex Lexer
    ~~~~~~~~~~~~~~~~~~
"""

import re

class TexLexer:
    """A very simple lexer for tex/latex code. Roughly follows the
    state machine descriped in Tex By Topic, Chapter 2.

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
        # XXX but tests reveal otherwise
        ('control', br'[\\]([a-zA-Z]+|[~' + br"'" + br'"` =^!])'),
        ('controlx', br'[\\][^a-zA-Z]'),
        # parameter tokens
        ('parameter', br'\#[0-9]'),
        # any remaining characters; for ease we also handle space and
        # newline as tokens
        ('space', b' '),
        ('newline', b'\n'),
        ('char', br'.'),
        ]

    def __init__(self):
        """Initialize regular expression string."""
        # three possible states:
        # newline (N), skipping spaces (S), and middle of line (M)
        self.state = 'N'
        # inline math mode?
        self.inline_math = False
        # maintain a buffer of tokens (lexed) and characters (to be
        # lexed on next iteration)
        self.token_buffer = []
        self.char_buffer = b''
        # regular expression used for matching
        self.regexp = re.compile(
            b"|".join(
                "(?P<%s>%s)" % (name, regexp)
                for name, regexp in self.tokens),
            re.DOTALL)

    def get_raw_tokens(self, bytes_):
        """Yield tokens without any further processing. Tokens are one of:

        - ``\\<word>``: a control word (i.e. a command)
        - ``\\<symbol>``: a control symbol (i.e. \\^ etc.)
        - ``#<n>``: a parameter
        - a single byte character
        """
        for match in self.regexp.finditer(bytes_):
            for name, regexp in self.tokens:
                token = match.group(name)
                if token is not None:
                    yield (name, token, match.start(), match.end())
                    break
            else:
                # should not happen
                raise AssertionError("lexer failed on '%s'" % text)

    def get_tokens(self, bytes_):
        """Yield tokens while maintaining a state. Also skip
        whitespace after control words and (some) control symbols.
        Replaces newlines by spaces and \\par commands depending on
        the context.
        """
        for name, token, start, end in self.get_raw_tokens(bytes_):
            if name == 'newline':
                if self.state == 'N':
                    # if state was 'N', generate new paragraph
                    yield 'control', b'\\par'
                elif self.state == 'S':
                    # switch to 'N' state, do not generate a space
                    self.state = 'N'
                elif self.state == 'M':
                    # switch to 'N' state, generate a space
                    self.state = 'N'
                    yield 'space', b' '
                else:
                    raise AssertionError(
                        "unknown tex state '%s'" % self.state)
            elif name == 'space':
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
                    yield name, token
                else:
                    raise AssertionError(
                        "unknown tex state '%s'" % self.state)
            elif name == 'char':
                self.state = 'M'
                # detect math mode
                if token == '$':
                    self.inline_math = not self.inline_math
                yield name, token
            elif name == 'parameter':
                self.state = 'M'
                yield name, token
            elif name == 'control':
                # go to space skip mode
                self.state = 'S'
                yield name, token
            elif name == 'controlx':
                # don't skip following space, so go to M mode
                self.state = 'M'
                yield name, token
            elif name == 'comment':
                # go to newline mode, no token is generated
                # note: comment includes the newline
                self.state = 'N'
