from sphinxcontrib.bibtex.latex_lexer import TexLexer

def test_tex_lexer(text_latex, tokens):
    lexer = TexLexer()
    #print(list(lexer.parse(text_latex)))
    #print(list(tokens))
    assert(list(lexer.get_tokens(text_latex)) == list(tokens))

test_tex_lexer(
    b'hello!  [#1] This \\is\\   \\^ a \ntest.\n    \nHey.\n\n\# x \#x',
    br'h|e|l|l|o|!| |[|#1|]| |T|h|i|s| |\is|\ |\^|a| '
    br'|t|e|s|t|.| |\par|H|e|y|.| '
    br'|\par|\#| |x| |\#|x'.split(b'|'))

