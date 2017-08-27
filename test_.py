import pyhama
import os
import PIL

INPUT_TEST_FILES = ("test.png", "test.jpg")
OUTPUT_FILE = "pegboard.png"


def clean():
    if os.path.isfile("pegboard.svg"):
        os.remove("pegboard.svg")
    if os.path.isfile("pegboard.png"):
        os.remove("pegboard.png")


def test():
    clean()
    for input_file in INPUT_TEST_FILES:
        pyhama.process(15, 15, 30, input_file)
        assert os.path.isfile(OUTPUT_FILE)
        im = PIL.Image.open(OUTPUT_FILE)
        assert im.size == (15*30, 15*30)
        clean()
