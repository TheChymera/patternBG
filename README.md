#patternBG

Python script which renders randomly tiled images.
This can be used to produce GNOME3-like background images or other decorative artwork.
The script can be interfaced with from the command line using the `patternBG_cli` command, and allows you to specify a plethora of parameters (see the "Usage" section below).

##Installation

####On [Gentoo Linux](http://en.wikipedia.org/wiki/Gentoo_linux) and [Derivatives](http://en.wikipedia.org/wiki/Category:Gentoo_Linux_derivatives):

patternBG is available in the [Portage](http://en.wikipedia.org/wiki/Portage_(software)) *[chymerc overlay](https://github.com/TheChymera/chymeric)* as **[app-misc/RTbatch](https://github.com/TheChymera/chymeric/tree/master/app-misc/RTbatch)**.
Just run the following command:

```
emerge RTbatch
```

*If you are not yet using this overlay, it can be enabled with just two commands, as seen in [the README](https://github.com/TheChymera/chymeric).*

####On all other Operating Systems:

For all other Linux distributions or operating systems, the package can easily be installed via [pip](http://en.wikipedia.org/wiki/Pip_(Python)).
This also handles all Python dependencies.

```
git clone https://github.com/TheChymera/patternBG.git your/local/repository/path
pip install [--user] -e your/local/repository/path
```

##Dependencies

* **[NumPy](https://en.wikipedia.org/wiki/Numpy)** - in [Portage](http://en.wikipedia.org/wiki/Portage_(software)) as **app-text/texlive**
* **[matplotlib](https://en.wikipedia.org/wiki/Matplotlib)** - in Portage as **dev-python/matplotlib**
* **[scikit-image](http://scikit-image.org/)** - in Portage as **sci-libs/scikits_image**
* **[OpenCV](http://en.wikipedia.org/wiki/Opencv)** - in Portage as **media-libs/opencv**

##Usage    
Run the script either as `patternBG_cli` (if installed globally), or as `./patternBG_cli.py` from the containing folder:
```
patternBG_cli   [-h] [-v HSV_VARIANCES HSV_VARIANCES HSV_VARIANCES]
		[-i INCREMENT_STYLES [INCREMENT_STYLES ...]] [-s STOP]
		[-d DROP_SHADOWS]
		[-p SHADOW_PARAMETERS SHADOW_PARAMETERS]
                [-l SHADOW_LENGTH] [-o OUTPUT] [-y] [-b BOOST_FIRST]
                dimensions dimensions HSVmeans HSVmeans HSVmeans
```

Example:
```
patternBG_cli 2560 1440 100 200 190 -y -v 1 2 2 -i vertical square -s 20 -d 6 -b 3

```

##Arguments:
```
positional arguments:
  dimensions            2 integers specifying the desired image width and
                        height. The width and height need a large non-prime
                        common divisor, preferably with at least 3 factors.
  HSVmeans              3 integers specifying the hue, saturation, and value
                        means respectively.

optional arguments:
  -h, --help            show this help message and exit
  -v HSV_VARIANCES HSV_VARIANCES HSV_VARIANCES, --HSV-variances HSV_VARIANCES HSV_VARIANCES HSV_VARIANCES
                        3 integers specifying the hue, saturation, and value
                        variances respectively ("full" wil apply the maximum
                        variance for the respective mean, without warping the
                        color space)
  -i INCREMENT_STYLES [INCREMENT_STYLES ...], --increment-styles INCREMENT_STYLES [INCREMENT_STYLES ...]
                        A list specifying the tiling mode (square, horizontal,
                        and vertical) for each tiling iteration in an ordinal
                        fashion: if the list is shorter than the tiling
                        increments the last attribute is repeated.
  -s STOP, --stop STOP  Pixel size of the smallest tile (tiling "stops" at
                        this level, value should be >= 1, but be careful, for
                        small values this may take a LOT of time).
  -d DROP_SHADOWS, --drop-shadows DROP_SHADOWS
                        Number of vertical drop shadows to apply to the image,
                        0 to apply none.
  -p SHADOW_PARAMETERS SHADOW_PARAMETERS, --shadow-parameters SHADOW_PARAMETERS SHADOW_PARAMETERS
                        2 integers specifying the maximal saturation and value
                        (in this order) adjustment for shadows - please make
                        sure that these numbers are evenly divided by
                        `shadow_increments`
  -l SHADOW_LENGTH, --shadow-length SHADOW_LENGTH
                        The number of increments (pixels) over which to fade
                        the shadow (please make sure that this number evenly
                        divides `shadow_parameters`).
  -o OUTPUT, --output OUTPUT
                        Save image to this location (if relative, the path is
                        calculated starting at `../patternBG/output/`).
  -y, --display         Set this if you want to view the image (via
                        Matplotlib) when the script executes.
  -b BOOST_FIRST, --boost-first BOOST_FIRST
                        How many fold to increase the variance for the first
                        (largest) set of tiles - this can be useful if you
                        want to create more contrast for shadows.
```


Released under the GPLv3 license.
Project led by Horea Christian (address all e-mail correspondence to: h.chr@mail.ru)
