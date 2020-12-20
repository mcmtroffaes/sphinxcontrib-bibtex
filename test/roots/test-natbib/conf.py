import os
import sys
sys.path.append(os.path.dirname(__file__))  # ensure natbib extension is found
extensions = ['natbib']
exclude_patterns = ['_build']
natbib = {
    'file': 'test.bib',
    'brackets': '[]',
    'separator': ',',
    'style': 'numbers',
    'sort': True,
}
