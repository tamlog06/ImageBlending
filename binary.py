import cv2
import os
import numpy as np
import argparse
from glob import glob


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image_dir', help='Path to image')
    parser.add_argument('-o', '--output_dir', help='Path to output')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    ext = ['jpg', 'png', 'jpeg']
    img_list = []
    for e in ext:
        img_list.extend(glob(os.path.join(args.image_dir + '/*.' + e)))

    for img_path in img_list:
        print(f"Processing {img_path}...")
        img_name = os.path.basename(img_path)
        img = cv2.imread(img_path, 0)
        ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite(os.path.join(args.output_dir, img_name), img)
