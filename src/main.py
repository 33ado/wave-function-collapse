from PIL import Image

from wfc import WFC


def main():
    sample = Image.open("samples/Maze.png")
    pat_size = 2
    out_size = 80
    wfc = WFC(
        sample_img=sample,
        pattern_size=pat_size,
        out_width=out_size,
        out_height=out_size,
    )

    while not wfc.collapse():
        wfc = WFC(sample, pat_size, out_size, out_size)

    out = wfc.render()
    out.save("output/result.png")
    out.show()


if __name__ == "__main__":
    main()
