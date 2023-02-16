"""ca_01.py: Starter file to run homework 1"""

__author__ = "Shishir Shah"
__version__ = "1.0.0"
__copyright__ = "Copyright 2022 by Shishir Shah, Quantitative Imaging Laboratory (QIL), Department of Computer  \
                Science, University of Houston.  All rights reserved.  This software is property of the QIL, and  \
                should not be distributed, reproduced, or shared online, without the permission of the author."


import sys
import matplotlib.pyplot as plt
from imageops import DSImage as DSImage
import logging


def image_display(image):
    if image.get_channels() == 3:
        plt.imshow(image.get_image_data())
        plt.axis('off')
        plt.show()
    else:
        plt.imshow(image.get_image_data(), cmap='gray', vmin=0, vmax=255)
        plt.axis('off')
        plt.show()
    return


def main():
    """ The main function that parses input arguments, calls the appropriate
     method and writes the output image"""

    # Initialize logging
    Log_Format = "%(levelname)s %(asctime)s - %(message)s"

    logging.basicConfig(filename="output/logfile.log",
                        filemode="w",
                        format=Log_Format,
                        level=logging.INFO)
    logger = logging.getLogger()
    # handler = logging.FileHandler('output/logfile.log')
    # logger.addHandler(handler)
    logger.info('Logging initialized.')

    # Parse input arguments
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the input image", metavar="IMAGE")

    parser.add_argument("-d", "--display", dest="display",
                        help="specify if images should be displayed", metavar="DISPLAY")

    args = parser.parse_args()

    # Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        logger.error('Input file name not specified.')
        sys.exit(1)
    if args.display is None or int(args.display) > 1:
        print("Please specify if images should be displayed or now")
        print("use the -h option to see usage information")
        logger.error('Image display option not correctly specified.')
        sys.exit(1)
    else:
        display = int(args.display)
        outputDir = 'output/'
        # Initialize image of type MyImage
        myimage = DSImage.MyImage()
        # Load Image specified in input argument
        try:
            myimage.load_image(args.image)
            logger.info('Image loading succeeded.')
        except:
            logger.error('Error loading image.')
            sys.exit(1)
        if display == 1:
            image_display(myimage)
        # Save Image
        output_image_name = outputDir + 'input_image' + '.ppm'
        try:
            myimage.save_image(output_image_name)
            logger.info('Image saving succeeded.')
        except:
            logger.error('Error saving image.')
            sys.exit(1)

        # Create a new image of size 512 x 256 with all pixels set to blue
        try:
            myimage.new_image(512, 256, [0, 0, 255])
            logger.info('Creating of new color image succeeded.')
        except:
            logger.error('Error creating new color image.')
            sys.exit(1)

        if display == 1:
            image_display(myimage)
        output_image_name = outputDir + 'blue_image' + ".ppm"
        myimage.save_image(output_image_name)

        # Create a new image of size 512 x 256 with all pixels set to 128
        try:
            myimage_gray = DSImage.MyImage()
            myimage_gray.new_image(512, 256, [128])
            logger.info('Creating of new gray scale image succeeded.')
        except:
            logger.error('Error creating new gray scale image.')
            sys.exit(1)

        if display == 1:
            image_display(myimage_gray)
        output_image_name = outputDir + 'gray_image' + ".pgm"
        try:
            myimage_gray.save_image(output_image_name)
            logger.info('Gray scale image saving succeeded.')
        except:
            logger.error('Error saving gray scale image.')
            sys.exit(1)

        # Check functions to get image width and height
        try:
            w = myimage.get_width()
            if w == 512:
                logger.info('Image width information is correct.')
            else:
                raise ValueError
        except:
            logger.error('Image width is incorrect.')
            sys.exit(1)

        try:
            h = myimage.get_height()
            if h == 256:
                logger.info('Image height information is correct.')
            else:
                raise ValueError
        except:
            logger.error('Image height is incorrect.')
            sys.exit(1)

        # Change a block of image pixels to white
        try:
            myimage.set_image_pixels([10, 10, 20, 40], [255, 255, 0])
            logger.info('Successfully changed sub-image pixel values.')
        except:
            logger.error('Error changing sub-image pixel values.')
            sys.exit(1)
        if display == 1:
            image_display(myimage)
        output_image_name = outputDir + 'blue_red_image' + ".ppm"
        myimage.save_image(output_image_name)

        try:
            v = myimage.get_image_pixel(15, 25)
            if len(v) == 3 and v[0] == 255 and v[1] == 255 and v[2] == 0:
                logger.info('Correct image pixel value verified.')
            else:
                raise ValueError
        except:
            logger.error('Error in getting or setting of pixel value.')
            sys.exit(1)

        # Convert image to gray level
        try:
            myimage.color_to_gray()
            v = myimage.get_image_pixel(15, 25)
            if v == 170:
                logger.info('Conversion of color to gray scale image succeeded.')
            else:
                raise ValueError
        except:
            logger.error('Error in converting color image to gray scale image.')
            sys.exit(1)
        if display == 1:
            image_display(myimage)
        output_image_name = outputDir + 'blue_red_gray_image' + ".pgm"
        myimage.save_image(output_image_name)

        # Compute the histogram of the gray level image
        try:
            myimage.gray_histogram()
            v = myimage.gray_hist[170]
            n = myimage.gray_hist[85]
            if v == 800 and n == 130272:
                logger.info('Computing of gray scale image histogram succeeded.')
            else:
                raise ValueError
        except:
            logger.error('Error in computing gray scale image histogram.')
            sys.exit(1)

        # Threshold image
        try:
            myimage.threshold_gray(100)
            v = myimage.get_image_pixel(15, 25)
            if v == 255:
                logger.info('Thresholding of gray scale image succeeded.')
            else:
                raise ValueError
        except:
            logger.error('Error in thresholding gray scale image.')
            sys.exit(1)
        if display == 1:
            image_display(myimage)
        output_image_name = outputDir + 'binary_image' + ".pgm"
        myimage.save_image(output_image_name)



if __name__ == "__main__":
    main()
