#!/use/bin/env python

import sys, json, numpy as np
import base64, cv2, argparse, os
#from PIL import Image
import imageio, numpy as np, scipy.ndimage, matplotlib.pyplot as plt

##ap = argparse.ArgumentParser()
##ap.add_argument("-i", "--image", required=True, help="Input base64 image to be processed.")
##args = vars(ap.parse_args())
##global image64
##image64 = args["image"]

def main():

	# Decoding the base64 to a full image.
	##image_data = base64.b64decode(image64) 
	##with open("WIP.jpg", 'wb') as f:
	##	f.write(image_data)
	##f.close()
	img_path = 'WIP.jpg'
	cv2.imshow("IMAGE", cv2.imread(img_path))
	cv2.waitKey(0)
	image = cv2.imread('WIP.jpg')
	#ip_pipeline1(image)
	canny(image)
	

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

def canny(image):
	grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cannied = cv2.Canny(grayscale, 100, 200)
	cv2.imshow('Cannied', cannied)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()

	img, canny_contours, hierarchy = cv2.findContours(cannied, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	stencil = np.zeros(image.shape).astype(image.dtype)
	mid_image = cv2.drawContours(stencil, canny_contours, -1, (0, 255, 0), 6)
	cv2.imshow('Intermediate', mid_image)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()

	mid_image = cv2.cvtColor(mid_image, cv2.COLOR_RGB2GRAY)
	#cv2.imwrite("stencil.jpg", mid_image)

	final, final_contours, hierarchy = cv2.findContours(mid_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	cv2.imshow('Final Image', final)
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()
	cv2.imwrite("final.bmp", final)
	os.system("python img-to-gcode.py final.BMP")

	c = max(final_contours, key=cv2.contourArea) #max contour
	f = open('path.svg', 'w+')
	f.write('<svg width="'+str(100)+'" height="'+str(100)+'" xmlns="http://www.w3.org/2000/svg">')
	f.write('<path d="M')

	for i in range(len(c)):
	    #print(c[i][0])
	    x, y = c[i][0]
	    print(x)
	    f.write(str(x)+  ' ' + str(y)+' ')

	f.write('"/>')
	f.write('</svg>')
	f.close()

	##TODO: re-process the filter on the thicker lines.

if __name__ == '__main__':
	main()

