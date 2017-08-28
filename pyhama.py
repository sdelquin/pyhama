"""PyHama

Usage:
    pyhama [--pb_width=<pbw>] [--pb_height=<pbh>] [--beadsize=<bs>] INPUT

Options:
    -h --help           Show this screen
    --pb_width=<pbw>    Pegboard size (measured in beads) [default: 18]
    --pb_height=<pbh>   Pegboard size (measured in beads) [default: 18]
    --beadsize=<bs>     Bead size (measured in pixels) [default: 30]
    INPUT               Input image
"""

import PIL
import jinja2
import cairosvg
from docopt import docopt
from fabulous.color import bold, magenta, green

PEGBOARD_TEMPLATE = "pegboard.tmpl.svg"
PEGBOARD_RENDERED = "pegboard.svg"
PEGBOARD_OUTPUT = "pegboard.png"


def process(pegboard_width, pegboard_height, beadsize, input_filename):
    im = PIL.Image.open(input_filename)
    resized_im = im.resize((pegboard_width, pegboard_height))
    radius = beadsize / 2
    beads = []
    for x in range(pegboard_width):
        for y in range(pegboard_height):
            info = resized_im.getpixel((x, y))
            if len(info) == 3:
                rgb, alpha = info, 1
            else:
                rgb, alpha = info[:3], round(info[3] / 100)
            rgba = (*rgb, alpha)
            beads.append({
                "x": (x * beadsize) + radius,
                "y": (y * beadsize) + radius,
                "rgba": rgba
            })
    viewbox = {
        "width": pegboard_width * beadsize,
        "height": pegboard_height * beadsize
    }
    radius = {
        "major": radius,
        "minor": radius * 0.4
    }

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=".")
    )
    template = jinja_env.get_template(PEGBOARD_TEMPLATE)
    rendered_template = template.render(
        viewbox=viewbox,
        radius=radius,
        beads=beads
    )
    with open(PEGBOARD_RENDERED, "w") as f:
        f.write(rendered_template)
    cairosvg.svg2png(url=PEGBOARD_RENDERED, write_to=PEGBOARD_OUTPUT)
    print(
        green("Done! ") +
        "Hama beads output template in: " +
        bold(magenta(PEGBOARD_OUTPUT))
    )


if __name__ == "__main__":
    arguments = docopt(__doc__)
    process(
        int(arguments["--pb_width"]),
        int(arguments["--pb_height"]),
        int(arguments["--beadsize"]),
        arguments["INPUT"]
    )
