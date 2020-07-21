from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name = 'leidenmark',
    version = '0.1.9',
    description = 'A markdown extension for converting Leiden+ epigraphic text to TEI Epidoc XML',
    packages = find_packages(),
    install_requires = ['markdown', 'lxml>=4.5', 'regex'],
    keywords = 'Leiden+ Markdown TEI Epidoc XML HTML',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = "https://github.com/andredelft/leidenmark",
    python_requires = '>=3.6',
    author = 'André van Delft',
    author_email = 'andrevandelft@outlook.com',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3'
    ]
)
