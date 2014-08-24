#!/usr/bin/python
__author__ = 'Horea Christian'
import argparse
import patternBG
import inspect

parser = argparse.ArgumentParser()
parser.add_argument("dimensions", help="2 integers specifying the desired image width and height. The width and height need a large non-prime common divisor, preferably with at least 3 factors.", nargs=2, type=int)
parser.add_argument("HSVmeans", help="3 integers specifying the hue, saturation, and value means respectively.", nargs=3, type=int)
parser.add_argument("-v", "--HSV-variances", help="3 integers specifying the hue, saturation, and value variances respectively (\"full\" wil apply the maximum variance for the respective mean, without warping the color space)", default=["full", "full", "full"], nargs=3)
parser.add_argument("-i", "--increment-styles", help="A list specifying the tiling mode (square, horizontal, and vertical) for each tiling iteration in an ordinal fashion: if the list is shorter than the tiling increments the last attribute is repeated.", default=["square"], nargs="+")
parser.add_argument("-s", "--stop", help="Pixel size of the smallest tile (tiling \"stops\" at this level, value should be >= 1, but be careful, for small values this may take a LOT of time).", type=int, default=10)
parser.add_argument("-d", "--drop-shadows", help="Number of vertical drop shadows to apply to the image, 0 to apply none.", type=int, default=0)
parser.add_argument("-p", "--shadow-parameters", help="2 integers specifying the maximal saturation and value (in this order) adjustment for shadows - please make sure that these numbers are evenly divided by `shadow_increments`", type=int, default=[-30,-50], nargs=2)
parser.add_argument("-l", "--shadow-length", help="The number of increments (pixels) over which to fade the shadow (please make sure that this number evenly divides `shadow_parameters`).", type=int, default=10)
parser.add_argument("-o", "--output", help="Save image to this location (if relative, the path is calculated starting at `../patternBG/output/`).", default="image.png")
parser.add_argument("-y", "--display", help="Set this if you want to view the image (via Matplotlib) when the script executes.", action="store_true")
parser.add_argument("-b", "--boost-first", help="How many fold to increase the variance for the first (largest) set of tiles - this can be useful if you want to create more contrast for shadows.", type=int, default=2)
args = parser.parse_args()

patternBG.patternBG(args.dimensions, args.HSVmeans, hsv_variances=map(int, args.HSV_variances), increment_styles=args.increment_styles, stop=args.stop, drop_shadows=args.drop_shadows, shadow_parameters=args.shadow_parameters, shadow_length=args.shadow_length, output=args.output, display=args.display, boost_first=args.boost_first)
