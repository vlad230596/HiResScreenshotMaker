import glob
import time

import cv2

from pathlib import Path

from stitching.blender import Blender
from EniPy.imageUtils import getBlankImage

class ImageRegion:
    def __init__(self, path):
        self.raw_image = cv2.imread(path)
        self.x, self.y = [int(p_str) for p_str in Path(path).stem.split("_")]

def processImage(path):
    images_path = glob.glob(f'{path}/*.png')
    start_time = time.time()

    regions = [ImageRegion(path) for path in images_path]
    print(f"Loaded images by: {time.time() - start_time:.2f} seconds")
    blender = Blender("no")
    imgs = [region.raw_image for region in regions]
    sizes = [(img.shape[1], img.shape[0]) for img in imgs]
    corners = [(region.x, region.y) for region in regions]
    masks = [getBlankImage(width, height, 255, 1) for width, height in sizes]
    print(f"Prepared data: {time.time() - start_time:.2f} seconds")
    blender.prepare(corners, sizes)
    for img, mask, corner in zip(imgs, masks, corners):
        blender.feed(img, mask, corner)
    print(f"Blender ready: {time.time() - start_time:.2f} seconds")
    blended = blender.blend()
    cv2.imwrite(f'results/{Path(path).name}.png', blended[0])
    print(f"Completed by: {time.time() - start_time:.2f} seconds")

processImage(f'images/50x50')