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

The output of the above lines is the following XML snippet (manually indented):

```xml
<div n="r" type="textpart">
  <ab>
    <l n="1">Lorem ipsum dolor</l>
    <l n="2">sit amet, con<gap precision="low" quantity="3" unit="character"></gap>c</l>
    <l break="no" n="3">etur adipiscing</l>
  </ab>
</div>
<div n="v" type="textpart">
  <ab>
    <gap quantity="2" unit="line"></gap>
    <l n="6">ut labore et dol</l>
    <l break="no" n="7">ore magna aliqua</l>
  </ab>
</div>
```
