import os
import numpy as np
import pandas as pd
import json
import math
from glob import glob
###step2 - to link cell loc with spot loc

def save_cellLoc_spotBarcode(single_cell_path, st_spot_path, st_json_file_path):
    single = pd.read_csv(single_cell_path)
    spot = pd.read_csv(st_spot_path)
    with open(st_json_file_path, 'r') as file:
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


if __name__ == "__main__":
    single_cell = 'path_to_4cell_class_CellPos'
    st_data = 'path_to st_data_with_the_sampleID_as_the_folder_name'
    files = sorted(glob(f"{single_cell}/*.csv"))
    for file in files:
        file_name = os.path.basename(file)[:-4]
        st_spot = glob(os.path.join(st_data, file_name, '*.csv'))[0]
        st_json = glob(os.path.join(st_data, file_name, '*.csv'))[0]
        save_cellLoc_spotBarcode(file, st_spot, st_json)