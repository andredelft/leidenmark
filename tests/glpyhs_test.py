from leidenmark import leiden_plus


def test_glyphs():
    assert leiden_plus('*slanting-stroke*') == '<g type="slanting-stroke"/>'
    assert leiden_plus('*tripunct?*') == '<unclear><g type="tripunct"/></unclear>'
    assert leiden_plus('*tripuncts*') == '<hi rend="italic">tripuncts</hi>'
