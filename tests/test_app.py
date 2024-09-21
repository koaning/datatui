def test_arxiv_example(snap_compare):
    assert snap_compare("examples/arxiv.py")

def test_image_example(snap_compare):
    assert snap_compare("examples/image.py")