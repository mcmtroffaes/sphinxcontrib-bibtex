"""
    Simple Tex Lexer
    ~~~~~~~~~~~~~~~~~~
"""

import re

class Token:
    """Stores information about a matched token."""

    def __init__(self, name, text, start, end):
        self.name = name
        self.text = text
        self.start = start
        self.end = end

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
        ]

    def __init__(self):
        """Initialize regular expression string."""
        # three possible states:
        # newline (N), skipping spaces (S), and middle of line (M)
        self.state = 'N'
        # inline math mode?
        self.inline_math = False
        # regular expression used for matching
        self.regexp = re.compile(
            b"|".join(
                b"(?P<%s>%s)" % (name, regexp)
                for name, regexp in self.tokens),
            re.DOTALL)

    def get_raw_tokens(self, bytes_):
        """Yield tokens without any further processing. Tokens are one of:

        - ``\\<word>``: a control word (i.e. a command)
        - ``\\<symbol>``: a control symbol (i.e. \\^ etc.)
        - ``#<n>``: a parameter
        - a series of byte characters
        """
        for match in self.regexp.finditer(bytes_):
            for name, regexp in self.tokens:
                text = match.group(name)
                if text is not None:
                    yield Token(name, text, match.start(), match.end())
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
        for token in self.get_raw_tokens(bytes_):
            if token.name == 'newline':
                if self.state == 'N':
                    # if state was 'N', generate new paragraph
                    yield Token('control', '\\par', token.start, token.end)
                elif self.state == 'S':
                    # switch to 'N' state, do not generate a space
                    self.state = 'N'
                elif self.state == 'M':
                    # switch to 'N' state, generate a space
                    self.state = 'N'
                    yield Token('space', b' ', token.start, token.end)
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
