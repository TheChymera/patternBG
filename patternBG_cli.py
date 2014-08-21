#!/usr/bin/python
__author__ = 'Horea Christian'
import argparse
import patternBG
import inspect

parser = argparse.ArgumentParser()
parser.add_argument("dimensions", help="2-item list of the desired image width and height. The width and height need a large non-prime common divisor, preferably with at least 3 factors.", type=int)
parser.add_argument("HSV means", help="A 3-item list of integers specifying hue, saturation, and value means respectively.", type=int)
parser.add_argument("-v", "--HSV-variances", help="A 3-item list of integers specifying hue, saturation, and value variances respectively (\"full\" wil apply the maximum variance for the respective mean, without warping the color space)", default=["full", "full", "full"])
parser.add_argument("-i", "--increment-styles", help="A list specifying the tiling mode (square, horizontal, and vertical) for each tiling iteration in an ordinal fashion: if the list is shorter than the tiling increments the last attribute is repeated.", default=["square"])
parser.add_argument("-s", "--stop", help="Pixel size of the smallest tile (tiling \"stops\" at this level, value should be >= 1, but be careful, for small values this may take a LOT of time)", default=["square"])


