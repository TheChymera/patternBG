from distutils.core import setup
setup(
    name="openBG",
    version="",
    description = "Python script that creates tile-based visual art. ",
    author = "Horea Christian",
    author_email = "chr@chymera.eu",
    url = "https://github.com/TheChymera/patternBG",
    keywords = ["artwork", "image processing"],
    py_modules = ["patternBG", "patternBG_cli"],
    classifiers = [],
    install_requires=[
	"pyopencv"
	"numpy"
	"matplotlib"
	"scikit-image"
    ],
    )
