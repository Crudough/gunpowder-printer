#!/use/bin/env python

import sys, json, numpy as np
import base64, cv2, argparse, os
#from PIL import Image
import imageio, numpy as np, scipy.ndimage, matplotlib.pyplot as plt
from stl_tools import numpy2stl
from scipy.misc import imresize
from scipy.ndimage import gaussian_filter

ap = argparse.ArgumentParser()
ap.add_argument("-if", "--imagefile", required=True, help="Input base64 image to be processed.")
args = vars(ap.parse_args())
global image64
image64 = args["imagefile"]

def main():

	# Decoding the base64 image from a text file to a full image useable by Opencv.
	with open(image64, 'rb') as b:
		image_file = b.read()
		img_data = base64.b64decode(image_file)
	
	import64 = open('WIP.jpg', 'wb')
	import64.write(img_data)
	img_path = 'WIP.jpg'
	cv2.imshow("IMAGE", cv2.imread(img_path))
	cv2.waitKey(0)
	image = cv2.imread('WIP.jpg')
	# Transfer fully decoded image to Image Processing Pipeline.
	canny(image)

def convert():
	A = cv2.imread('inverted_final.bmp')
	A = A.mean(axis=2)
	A = gaussian_filter(A.max() - A, 1.)

	numpy2stl(A, "CONVERTED_STL.stl", scale=0.2, mask_val = 5.)

def canny(image):
	'''PRE-PROCESSING'''
	grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cannied = cv2.Canny(grayscale, 100, 200)
	thresh1, inverted_canny = cv2.threshold(cannied, 127, 255, cv2.THRESH_BINARY_INV)
	cv2.imshow('Cannied', cannied)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()

	canny_contours, hierarchy = cv2.findContours(cannied, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	stencil = np.zeros(image.shape).astype(image.dtype)
	mid_image = cv2.drawContours(stencil, canny_contours, -1, (0, 255, 0), 6)
	cv2.imshow('Intermediate', mid_image)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()

	mid_image = cv2.cvtColor(mid_image, cv2.COLOR_RGB2GRAY)

	'''FINAL CONTOUR FINDING'''
	final_contours, hierarchy = cv2.findContours(mid_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	thresh2, inverted = cv2.threshold(mid_image, 127, 255, cv2.THRESH_BINARY_INV)

	cv2.imshow('Final Inverted Image', inverted)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()
	cv2.imwrite("inverted_final.bmp", inverted_canny)

	c = max(final_contours, key=cv2.contourArea) #max contour

	'''FINAL CONVERSION TO STL FILE'''
	convert()

if __name__ == '__main__':
	main()

