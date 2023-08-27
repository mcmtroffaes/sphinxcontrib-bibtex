import sphinx.builders.latex.transforms

extensions = ["sphinxcontrib.bibtex"]
bibtex_bibfiles = ["sources.bib"]
latex_documents = [
    ("index", "test.tex", "Test", "Mr. Test", "manual"),
]


class DummyTransform(sphinx.builders.latex.transforms.BibliographyTransform):
    def run(self, **kwargs):
        pass


sphinx.builders.latex.transforms.BibliographyTransform = DummyTransform
