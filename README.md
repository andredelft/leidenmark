# LeidenMark

```shell
$ pip install leidenmark
```

A Python Markdown extension for converting Leiden+ epigraphic text to TEI XML/HTML. Inspired by the Brill plain text (BPT) format that aims to incorporate Leiden+ into a Markdown-based syntax.

```python
>>> from markdown import markdown
>>> from leidenmark import LeidenPlus
>>> content = """\
<D=.r<=
1. Lorem ipsum dolor
2. sit amet, con[ca.3]c
3.-etur adipiscing
=>=D>
<D=.v<=
lost.2lin
6. ut labore et dol
7.-ore magna aliqua
=>=D>"""
>>> markdown(content, extensions = [LeidenPlus()])
```

The output of the above lines is the following XML snippet:

```xml
<div n="r" type="textpart">
  <ab>
    <l n="1">Lorem ipsum dolor</l>
    <l n="2">sit amet, con<gap precision="low" quantity="3" unit="character"/>c</l>
    <l break="no" n="3">etur adipiscing</l>
  </ab>
</div>
<div n="v" type="textpart">
  <ab>
    <gap quantity="2" unit="line"/>
    <l n="6">ut labore et dol</l>
    <l break="no" n="7">ore magna aliqua</l>
  </ab>
</div>
```

## Configuration

Given that this is a Markdown extension, conventions like `*italics*` and `**bold**` will also be recognized an converted (these in particular will additionally be transformed to the TEI element [`<hi>`](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-hi.html)). Though these are _in principle_ not part of the Leiden+ syntax, _in practice_ the use of italics and boldface is still encountered a lot. Therefore, support is maintaned by default, which can be switched off by passing `strict = True`:

```python
>>> markdown(content, extensions = [LeidenPlus(strict = True)])
```

NB: The blockprocessors for paragraphs and ordered list are always switched off, because they interfere too much with Leiden+.
