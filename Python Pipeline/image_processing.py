#!/use/bin/env python

import sys, json, numpy as np
import base64, cv2

def read_data():
	input = sys.stdin.readlines()
	return input

def main():

	input_image = read_data()
	image = base64.b64decode(input_image)
	cv2.imshow('IMAGE', image)

if __name__ == '__main__':
	main()

