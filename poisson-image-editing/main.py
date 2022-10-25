"""
  Usage:
   python main.py argvs[1] argvs[2] argvs[3] argvs[4]
  
   argvs[1]  :  shadowed image dir
   argvs[2]  :  original image dir
   argvs[3]  :  output image dir
   argvs[4]  :  method name --> import, mix, average, flatten

"""


import os
import sys
import cv2
import numpy as np
import time
from glob import glob


## my function
import poissonimageediting as poisson
from mask import make_mask

print(__doc__)


### 1. prepare config
start = time.time() 
argvs = sys.argv
src_dir = argvs[1]
tar_dir = argvs[2]
output_dir = argvs[3]
method = argvs[4]
shadow_dir = os.path.join(output_dir, "shadow_mask")


### 2. for output
os.makedirs(output_dir, exist_ok=True)
os.makedirs(shadow_dir, exist_ok=True)

ext = ['jpg', 'png', 'jpeg']
src_list = []
for e in ext:
    src_list.extend(glob(os.path.join(src_dir, '*.' + e)))

src_list.sort()

### 3. for each image
for src_path in src_list:
    filename, ext = os.path.splitext( os.path.basename(src_path) )
    print(f"processing {src_path} ...")

    src_img = np.array(cv2.imread(src_path, 1)/255.0, dtype=np.float32)
    tar_path = os.path.join(tar_dir, f'{filename}{ext}')
    assert os.path.exists(tar_path), f"{tar_path} does not exist"
    tar_img = np.array(cv2.imread(tar_path, 1)/255.0, dtype=np.float32)

    ### 4. make mask
    mask_img = make_mask(src_img, tar_img)
    cv2.imwrite(os.path.join(shadow_dir, f'{filename}{ext}'), mask_img)

    ### 5. make output image
    blended, overlapped = poisson.poisson_blend(src_img, mask_img/255.0, tar_img, method)

    ### 6. save result
    output_path = os.path.join(output_dir, f'{filename}{ext}')
    cv2.imwrite(output_path, blended)
    print(f"save upscaled image as \n --> {output_path}")
