#!/use/bin/env python

import sys, json, numpy as np
import base64, cv2, argparse, os
import imageio, numpy as np, scipy.ndimage, matplotlib.pyplot as plt
from stl_tools import numpy2stl
from scipy.misc import imresize
from scipy.ndimage import gaussian_filter

def load_json(file_path):
    img_path = 'WIP.jpg'

    with open(file_path) as j:
        json_data = json.load(j)
    j.close()

    img_data = base64.b64decode(json_data["image64"])
    import64 = open(img_path, 'wb')
    import64.write(img_data)
    image = cv2.imread(img_path)

    return image

def convert():
    A = cv2.imread('inverted_final.bmp')
    A = A.mean(axis=2)
    A = gaussian_filter(A.max() - A, 1.)

    # Converting the processed image to an STL file.
    numpy2stl(A, "CONVERTED_STL.stl", scale=0.2, mask_val = 5.)
    # Converting STL file to G-Code representation.
    os.system("potrace -s inverted_final.bmp")
    os.system("juicy-gcode inverted_final.svg -o final_out.gcode")
    #os.system("slic3r CONVERTED_STL.stl --gcode-comments --skirts 0")
        
def canny(image):

    '''PRE-PROCESSING'''
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cannied = cv2.Canny(grayscale, 100, 200)
    thresh1, inverted_canny = cv2.threshold(cannied, 127, 255, cv2.THRESH_BINARY_INV)

    canny_contours, hierarchy = cv2.findContours(cannied, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    stencil = np.zeros(image.shape).astype(image.dtype)
    mid_image = cv2.drawContours(stencil, canny_contours, -1, (0, 255, 0), 6)
    mid_image = cv2.cvtColor(mid_image, cv2.COLOR_RGB2GRAY)

    '''FINAL CONTOUR FINDING'''
    final_contours, hierarchy = cv2.findContours(mid_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    thresh2, inverted = cv2.threshold(mid_image, 127, 255, cv2.THRESH_BINARY_INV)

    cv2.imwrite("inverted_final.bmp", inverted_canny)

def main():

    json_path = "exported.json"
    
    
    # Decoding the base64 image from a JSON file to a full image useable by Opencv.
    print("Loading image from JSON", end = '')
    loaded = load_json(json_path)
    print("...Done.")

    # Image Pre-processing
    print("Pre-processing original Base 64 Image", end = '')
    canny(loaded)
    print("...Done.")

    # Converting final processed 2D image to a 3D representation.
    print("Converting final image to 3D representation...")
    convert()
    print("Done!")
    sys.stdout.flush()

if __name__ == '__main__':
    main()

