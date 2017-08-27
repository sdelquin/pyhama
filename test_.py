import pyhama
import os
import PIL


def clean():
    if os.path.isfile("pegboard.svg"):
        os.remove("pegboard.svg")
    if os.path.isfile("pegboard.png"):
        os.remove("pegboard.png")


def test():
    clean()
    pyhama.process(15, 15, 30, "test.png")
    assert os.path.isfile("pegboard.png")
    im = PIL.Image.open("pegboard.png")
    assert im.size == (15*30, 15*30)
    clean()
