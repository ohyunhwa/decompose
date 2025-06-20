import argparse, glob, os, cv2
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

DEFAULT_IMAGE_DIR = os.path.join(SCRIPT_PATH, 'images/target')
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_PATH, 'images/target-contour-type1')

# opencv > B G R
color_red = (0, 0, 255)
color_blue = (255, 0, 0)
color_green = (0, 255, 0)

def separate(images_dir, output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(os.path.join(output_dir))
    
    images_list = sorted(glob.glob(os.path.join(images_dir, '*.png')))

    for i in range(len(images_list)):
        filename = os.path.splitext(os.path.basename(images_list[i]))[0]
        split_filename = filename.split('_')
        
        #fontno = split_filename[0]
        typeno = split_filename[1]
        #char_unicode = split_filename[2]
        
        if typeno == '1':
            img = cv.imread(images_list[i])
            assert img is not None, "file could not be read, check with os.path.exists()"
            gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
            ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
            
            # noise removal
            kernel = np.ones((3,3),np.uint8)
            opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 2)
            
            # sure background area
            sure_bg = cv.dilate(opening,kernel,iterations=3)
            
            # Finding sure foreground area
            dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
            ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)
            
            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            unknown = cv.subtract(sure_bg,sure_fg)
            
            # Marker labelling
            ret, markers = cv.connectedComponents(sure_fg)
            
            # Add one to all labels so that sure background is not 0, but 1
            markers = markers+1
            
            # Now, mark the region of unknown with zero
            markers[unknown==255] = 0
            
            markers = cv.watershed(img,markers)
            img[markers == -1] = [255,0,0]

            plt.imshow(markers)
            plt.show()
        elif typeno == '2':
            pass
        
        elif typeno == '3':
            pass
        
        elif typeno == '4':
            pass
        
        elif typeno == '5':
            pass
        
        elif typeno == '6':
            pass 
        
        else:
            print(f"No contours found in {images_list[i]}")
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--img_dir', type=str, dest='images_dir', default=DEFAULT_IMAGE_DIR)
    parser.add_argument('--output_dir', type=str, dest='output_dir', default=DEFAULT_OUTPUT_DIR)
    
    args = parser.parse_args()
    
    separate(args.images_dir, args.output_dir)
        
        