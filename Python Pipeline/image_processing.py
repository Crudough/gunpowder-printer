#!/use/bin/env python

import sys, json, numpy as np
import base64, cv2, argparse
from PIL import Image
import imageio, numpy as np, scipy.ndimage, matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Input base64 image to be processed.")
args = vars(ap.parse_args())
global image64
image64 = args["image"]

def main():

	# Decoding the base64 to a full image.
	image_data = base64.b64decode(image64) 
	with open("WIP.jpg", 'wb') as f:
		f.write(image_data)
	f.close()
	img_path = 'WIP.jpg'
	cv2.imshow("IMAGE", cv2.imread(img_path))
	cv2.waitKey(0)
	image = cv2.imread('WIP.jpg')
	ip_pipeline1(image)
	

def ip_pipeline1(image):
	# Preprocessing/Grayscaling
	grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(grayscale, 120, 255, cv2.THRESH_BINARY)

	# Find Contours
	im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key=cv2.contourArea, reverse=True)

	# TRIAL
	perimeters = [cv2.arcLength(contours[i],True) for i in range(len(contours))]
	listindex=[i for i in range(25) if perimeters[i]>perimeters[0]/2]
	numcards=len(listindex)
	stencil = np.zeros(image.shape).astype(image.dtype)
	cv2.drawContours(stencil, [contours[listindex[-1]]], 0, (255, 255, 255), cv2.FILLED)
	#cv2.drawContours(image, contours, -1, (0,255,0), 3)

	cv2.imshow('image', stencil)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()

	cv2.imshow('image', image)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()
	#cv2.imshow('IMAGE', image)

def ip_pipeline2(image):


if __name__ == '__main__':
	main()

