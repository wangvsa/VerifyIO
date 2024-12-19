# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'VerifyIO'
copyright = '2024, Chen Wang'
author = 'Chen Wang'

#release = '0.1'
#version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration', 'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output
html_theme = 'furo'

#Sphinx builds a tree of documents based on the toctree directives contained within the source files. This sets the name of the document containing the master toctree directive, and hence the root of the entire tree. Example:
#master_doc = 'contents'



# -- Options for EPUB output
epub_show_urls = 'footnote'
