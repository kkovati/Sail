import pandas as pd

import pathlib
path = pathlib.Path().absolute()
print(str(path) + '/buoy_coordinates.json')

df = pd.read_json(str(path) + '/buoy_coordinates.json')

for buoy_coords in df['2_race']:
    x = int(buoy_coords['x'])
    y = buoy_coords['y'])
    print(x,y)
