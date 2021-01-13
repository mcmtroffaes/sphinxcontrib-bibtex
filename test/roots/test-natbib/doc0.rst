doc0
----

Testing the various cite roles using default settings.

Some citations
:cite:t:`1657:huygens`
:cite:t:`joyce:1999`
:cite:t:`2011:troffaes:isipta:natext`
:cite:t:`1996:fukuda`
:cite:t:`2009:defra:animal:health`
:cite:t:`test:url`
:cite:t:`test:url2`
:cite:t:`2000:troffaes:msthesis`
:cite:t:`2008:hable:thesis`
:cite:t:`Sherwood`
:cite:t:`2005:cormack`
:cite:t:`RSI`
:cite:t:`Kristensen83`
:cite:t:`Astrom2005`
:cite:t:`noauthor`.

Multiple keys in text were analysed by
:cite:t:`1657:huygens,joyce:1999`.

Multiple keys in parenthesis
:cite:p:`1657:huygens,joyce:1999`.

For post text, we refer you to
:cite:t:`1657:huygens [p. 3]`.
For pre and post text,
:cite:t:`joyce:1999 [see][p. 20]`.
For pre text,
:cite:t:`joyce:1999 [see][]`.

Now the same with parenthesis style.
Here we use post text
:cite:p:`1657:huygens [p. 3]`.
Here we use pre and post text
:cite:p:`joyce:1999 [see][p. 20]`.
Here we use pre text
:cite:p:`joyce:1999 [see][]`.

All the commands with the same reference:

* p :cite:p:`Kristensen83`
* ps :cite:ps:`Kristensen83`
* alp :cite:alp:`Kristensen83`
* alps :cite:alps:`Kristensen83`
* t :cite:t:`Kristensen83`
* ts :cite:ts:`Kristensen83`
* alt :cite:alt:`Kristensen83`
* alts :cite:alts:`Kristensen83`
* author :cite:author:`Kristensen83`
* authors :cite:authors:`Kristensen83`
* year :cite:year:`Kristensen83`
* yearpar :cite:yearpar:`Kristensen83`
* text :cite:text:`Kristensen83`
* title :cite:title:`Kristensen83`

Title cite if there is no title :cite:title:`notitle`.

Another special case :cite:t:`branchtest`.
