from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
__author__ = 'Horea Christian'

def patternBG(dimensions, hsv_means, hsv_variances = ["full", "full", "full"], increment_styles=["square"], stop=10, drop_shadows=0, shadow_parameters=[-30,-50], shadow_length=10, output="image.png", display=False, boost_first=1):
	"""
	Function for creating randomly tiled images.
	The tiling is dome by dividing the image into tiles based on the width and height common divisors.
	The "coloring" of the tiles is done in HSV space based on user-specified means and variances.
	For each smaller level of tiles we re-apply random colorization within the bounds defined above. 
	
	Arguments:
	dimensions -- 2-item list specifying the width and height of the output image. 
	hsv_means -- A 3-item list of integers specifying hue, saturation, and value means respectively.	
	hsv_variances -- A 3-item list of integers specifying hue, saturation, and value variances respectively ("full" wil apply the maximum variance for the respective mean, without warping the color space).
	increment_styles -- A list specifying the tiling mode (square, horizontal, and vertical) for each tiling iteration in an ordinal fashion: if the list is shorter than the tiling increments the last attribute is repeated.
	stop -- Pixel size of the smallest tile (tiling "stops" at this level, value should be >= 1, but be careful, for small values this may take a LOT of time).
	drop_shadows -- Number of vertical drop shadows to apply to the image, `False` to apply none.
	shadow_parameters -- The maximal saturation and value (in this ordeer) adjustment for shadows - please make sure that these numbers are evenly divided by `shadow_length`.
	shadow_length -- The number of increments (pixels) over which to fade the shadow (please make sure that this number evenly divides `shadow_parameters`).
	output -- Save image to this location (if relative, the path is calculated starting at `../patternBG/output/`).
	display -- `True` if you want to view the image (via Matplotlib) when the script executes.
	boost_first -- How many fold to increase the variance for the first (largest) set of tiles - this can be useful if you want to create more contrast for shadows.
	"""
	from fractions import gcd
	import numpy as np
	import cv2
	from itertools import product
	from random import randrange
	from matplotlib import pyplot as plt
	from skimage.io import imsave
	from os.path import isabs, expanduser, isdir
	from os import makedirs
	
	width = dimensions[0]
	height = dimensions[1]
	max_tile_size = gcd(width, height)
	tile_increments = prime_factors(max_tile_size)
	
	img = np.ones((height,width,3), np.uint8)
	img[:,:,0] = img[:,:,0]*hsv_means[0]
	img[:,:,1] = img[:,:,1]*hsv_means[1]
	img[:,:,2] = img[:,:,2]*hsv_means[2]
	
	for ix, (mean, variance) in enumerate(zip(hsv_means, hsv_variances)):
		if variance == "full":
			hsv_variances[ix] = np.min([mean,255-mean])
	
	#add initial level (1) to the `tile_increments` (this level corresponds to clusters of `max_tile_size` size)
	tile_increments[:0] = [1]
	
	#use cartesian products to extend `tile_increments`
	compound_increments = []
	for increment_tuple in product(tile_increments, repeat=len(tile_increments)):
		compound_increment = 1
		for increment in increment_tuple:
			compound_increment *= increment
		compound_increments.append(compound_increment)
	compound_increments=sorted(list(set(compound_increments)))
	
	if 2 in compound_increments:
		compound_increments.remove(2) 
	
	#delete entries from increments list so that the smallest tile is not smaller than `stop`
	tile_increments = []
	for increment in compound_increments:
		if max_tile_size/increment >= stop:
			tile_increments.append(increment)
	
	#extend `increment_styles` list to match the length of `tile_increments` by repeating the last entry 
	if len(tile_increments) < len(increment_styles):
		increment_styles = increment_styles[:len(tile_increments)]
	if len(tile_increments) > len(increment_styles):
		increment_styles.extend([increment_styles[-1]]*(len(tile_increments)-len(increment_styles)))
		 
	for ix_s, increment in enumerate(tile_increments):
		tile_size = max_tile_size/increment
		if ix_s != 0:
			boost_first = 1
		for a in list(product(np.arange(width/tile_size),np.arange(height/tile_size))):
			w_offset = a[0]*tile_size
			h_offset = a[1]*tile_size
			if increment_styles[ix_s] == "square":
				for ix, variance in enumerate(hsv_variances):
					img[h_offset:h_offset+tile_size,w_offset:w_offset+tile_size,ix] = img[h_offset:h_offset+tile_size,w_offset:w_offset+tile_size,ix]+np.rint(randrange(-variance*999,variance*999+1)/999)*boost_first
			elif increment_styles[ix_s] == "vertical":
				if h_offset != 0: # we don't want to apply color transformation on all the square regions of the `a` product space (otherwise we'll over-apply it)
					continue
				for ix, variance in enumerate(hsv_variances):
					img[:,w_offset:w_offset+tile_size,ix] = img[:,w_offset:w_offset+tile_size,ix]+np.rint(randrange(-variance*999,variance*999+1)/999)*boost_first
			elif increment_styles[ix_s] == "horizontal":
				if w_offset != 0: # we don't want to apply color transformation on all the square regions of the `a` product space (otherwise we'll over-apply it)
					continue
				for ix, variance in enumerate(hsv_variances):
					img[h_offset:h_offset+tile_size,:,ix] = img[h_offset:h_offset+tile_size,:,ix]+np.rint(randrange(-variance*999,variance*999+1)/999)*boost_first
			else:
				raise NameError("The `increment_styles` value \""+ increment_styles[ix_s]+"\" is not covered by the script. Aborting.")
	
	if drop_shadows:
		contrasts = []
		directions = []
		for primary_divider in np.arange(width/max_tile_size)[:-1]+1:
			contrast = 0
			#here we slice just the divider rows (last row of last tile and first row of next tile) to lessen the load
			segment_start = int(primary_divider*max_tile_size-1)
			segment_end = int(primary_divider*max_tile_size+1)
			divider_rows = img[:,segment_start:segment_end,:]
			divider_rows = cv2.cvtColor(divider_rows,cv2.COLOR_HSV2RGB) #no direct HSV2LAB conversion so we have to do this :-/
			divider_rows = cv2.cvtColor(divider_rows,cv2.COLOR_RGB2LAB)
			for i in np.arange(height):
				contrast += np.sqrt(sum((divider_rows[i,0,:] - divider_rows[i,1,:])**2))
			contrasts.append(contrast)
			
			#determine in which direction the shadows should go (light areas go to the foreground)
			L_contrast = sum(divider_rows[:,0,1]) - sum(divider_rows[:,1,1])
			if L_contrast >= 0:
				directions.append("left")
			else:
				directions.append("right")
		
		for shadow_ix in np.array(contrasts).argsort()[-drop_shadows:][::-1]+1:
			if directions[shadow_ix-1] == "right":
				direction = 1
				invert_offset = 0
			else:
				direction = -1
				invert_offset = -1
			for increment in np.arange(shadow_length):
				img[:,shadow_ix*max_tile_size+increment*direction+invert_offset,1] = img[:,shadow_ix*max_tile_size+increment*direction+invert_offset,1] + (shadow_parameters[0]/shadow_length*(shadow_length-increment))
			for increment in np.arange(shadow_length):
				img[:,shadow_ix*max_tile_size+increment*direction+invert_offset,2] = img[:,shadow_ix*max_tile_size+increment*direction+invert_offset,2] + (shadow_parameters[1]/shadow_length*(shadow_length-increment))
	
	#convert image to RGB for plotting and saving:
	img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
	
	#save image here:
	output = expanduser(output)
	if isabs(output):
		imsave(output, img)
	else:
		if not isdir ("output/"):
			makedirs("output/")
		imsave("output/"+output, img)
		
	#display via matplotlib:
	if display:
		plt.imshow(img,'gray')
		plt.axis('off')
		plt.show()

def prime_factors(n):
	"""Returns all the prime factors of a positive integer"""
	factors = []
	d = 2
	while n > 1:
		while n % d == 0:
			factors.append(d)
			n /= d
		d = d + 1

	return factors

if __name__ == "__main__":
	patternBG([2560, 1440], [100,200,190], [1,2,1], increment_styles=["vertical","square"], stop=20, drop_shadows=5, display=True)
