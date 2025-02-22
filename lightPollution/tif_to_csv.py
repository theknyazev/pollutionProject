from osgeo import gdal, osr
from PIL import Image
import pandas as pd

gdal.DontUseExceptions()
Image.MAX_IMAGE_PIXELS = None


filename = "Harmonized_DN_NTL_2021_simVIIRS.tif"
dataset = gdal.Open(filename)

img = Image.open(filename)
rgb_img = img.convert('RGB')

df = pd.DataFrame(columns=['Pixel_X', 'Pixel_Y', 'Longitude', 'Latitude', 'brightness'])

gt = dataset.GetGeoTransform()

width = dataset.RasterXSize
height = dataset.RasterYSize

srs = osr.SpatialReference()
srs.ImportFromWkt(dataset.GetProjection())

data_list = []

for y in range(4200):
    for x in range(1406):
        lon = gt[0] + x * gt[1] + y * gt[2]
        lat = gt[3] + x * gt[4] + y * gt[5]

        point = osr.CoordinateTransformation(srs, srs.CloneGeogCS()).TransformPoint(lon, lat)

        try:
            pixel = rgb_img.getpixel((x, y))
        except:
            pixel = ['NaN']

        # print(f"Pixel at ({x}, {y}) corresponds to ({point[0]}, {point[1]})")
        # print(pixel)

        data_list.append(
            {'Pixel_X': x, 'Pixel_Y': y, 'Longitude': point[0], 'Latitude': point[1], 'Brightness': pixel[0]})


    for x in range(23761, width):
        lon = gt[0] + x * gt[1] + y * gt[2]
        lat = gt[3] + x * gt[4] + y * gt[5]

        point = osr.CoordinateTransformation(srs, srs.CloneGeogCS()).TransformPoint(lon, lat)

        try:
            pixel = rgb_img.getpixel((x, y))
        except:
            pixel = ['NaN']

        # print(f"Pixel at ({x}, {y}) corresponds to ({point[0]}, {point[1]})")
        # print(pixel)

        data_list.append(
            {'Pixel_X': x, 'Pixel_Y': y, 'Longitude': point[0], 'Latitude': point[1], 'Brightness': pixel[0]})

df = pd.DataFrame(data_list, columns=['Pixel_X', 'Pixel_Y', 'Longitude', 'Latitude', 'Brightness'])

df.to_csv('output.csv', index=False)
print(df.head())
