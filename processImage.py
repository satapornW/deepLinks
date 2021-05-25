#This file will be used to process images for sameness
from PIL import ImageChops, Image
import math, operator



def rmsdiff(im1, im2):

	'''
	Calculate the root-mean-square difference between two images
	Same image should return the value of 0.0
	Max different value should be 441.0
	Some value to consider to establish acceptable value range.
	Time diffence: 8.0
	Saved button: 23.0
	Saved and like: 52.0
	Item vs profile: 255.0
	Similar color pallet item: 80.0
	
	'''
	h = ImageChops.difference(im1, im2).histogram()
	sq = (value*((idx%256)**2) for idx, value in enumerate(h))
	sum_of_squares = sum(sq)
	rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
	return rms

im1 = Image.open("itemControl.jpg")
im2 = Image.open("itemVariant1.jpg")
im3 = Image.open("littleSavedLiked.jpg")
im4 = Image.open("littleSavedLikedTime.jpg")

white = Image.open("white.jpg")
black = Image.open("black.jpg")

theOffice = Image.open("theOffice.jpg")
profile = Image.open("profile.jpg")
reignOfFire = Image.open("reignOfFire.jpg")

print "white vs black", rmsdiff(black, white)