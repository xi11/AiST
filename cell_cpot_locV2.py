import numpy as np
import pandas as pd
import json
import math
###step2 - to link cell loc with spot loc
# Read data
spot = pd.read_csv('/Users/xiaoxipan/Documents/project/st_crc/data_batch2/crc_D8/D8_Spatial-Projection.csv')
single = pd.read_csv('/Volumes/xpan7/project/AIheST/stCRC_wenyi_batch2/til/4_cell_class_refine/CellPos/S22-038036-D8-uncrop.tiff.csv')
json_file_path = '/Users/xiaoxipan/Documents/project/st_crc/data_batch2/crc_D8/scalefactors_json.json'

# Read JSON for diameter
with open(json_file_path, 'r') as file:
    diameter = json.load(file)['spot_diameter_fullres']


def are_pixels_within_circle(pixels_x, pixels_y, circle_center_x, circle_center_y, circle_radius):
    distances = np.sqrt((pixels_x - circle_center_x) ** 2 + (pixels_y - circle_center_y) ** 2)
    return distances < circle_radius


offset = 1
half = np.floor(diameter / 2) + offset
print(half)
spot_area = 3.14 * half * half


for _, row in spot.iterrows():
    x0, y0 = row['X Coordinate'], row['Y Coordinate']
    within_circle = are_pixels_within_circle(single['x_fullres'], single['y_fullres'], x0, y0, half)
    single.loc[within_circle, 'Barcode'] = row['Barcode']

single['spot_area'] = spot_area
single.to_csv('/Users/xiaoxipan/Documents/project/st_crc/data_batch2/output/D8_spatial_cell_visium_refine_spot.csv', index=False)
