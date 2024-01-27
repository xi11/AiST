import numpy as np
import os
import pandas as pd
import json
from glob import glob
import math
###step2 - to link cell loc with spot loc

spot = pd.read_csv('/Users/xiaoxipan/Documents/project/st_crc/data_batch1/crc_B5/B5_Spatial-Projection.csv')
single = pd.read_csv('/Volumes/xpan7/project/AIheST/stCRC_wenyi/til/4_cell_class_refine/CellPos/S22-008191-B5.tiff.csv')
json_file_path = '/Users/xiaoxipan/Documents/project/st_crc/data_batch1/crc_B5/B5_scalefactors_json.json'
single['Barcode'] = 'NA'
#single['spot_area'] = 'NA'
#spot_diameter_fullres: 258.77704 pixel, half = 129, P10, P14
#"spot_diameter_fullres": 238.67407188374798, half=119, P6

with open(json_file_path, 'r') as file:
    data = json.load(file)
    diameter = data['spot_diameter_fullres']
def is_pixel_within_circle(pixel_x, pixel_y, circle_center_x, circle_center_y, circle_radis):
    distance = math.sqrt((pixel_x - circle_center_x)**2 + (pixel_y - circle_center_y)**2)
    return distance < circle_radis

offset = 1  # larger vals indicate more expansion
half = np.floor(diameter/2) + offset
print(half)
for i in range(len(spot)):
    x0 = spot['X Coordinate'][i]
    y0 = spot['Y Coordinate'][i]
    single['Barcode'][single.apply(lambda row: is_pixel_within_circle(row['x_fullres'], row['y_fullres'], x0, y0, half), axis=1)] = spot['Barcode'][i]

single['spot_area'] = 3.14 * half * half
single.to_csv('/Users/xiaoxipan/Documents/project/st_crc/data_batch1/output/B5_spatial_cell_visium_refine_spot.csv', index=False)




