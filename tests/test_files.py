def test_rstrip():
    x = "Všechno nejlepši k narozeninam.md"
    assert x.removesuffix(".md") == "Všechno nejlepši k narozeninam"
