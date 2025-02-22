import pandas as pd
import pymap3d as pm
from math import sqrt
from scipy.spatial import KDTree

df = pd.read_stata("panel_year_v4_coord.dta")
original_df = pd.read_stata("panel_year_v4_coord.dta")

df = df.drop_duplicates(subset=['latitude', 'longitude'])
df = df.dropna(subset=['latitude', 'longitude'])

# 2020

points = pd.read_csv('PM2_5_NT_2023_GRID_2020.txt', delimiter=';')
points_ru = points.loc[points.ISO2 == 'RU']

latitude0 = 57.262282
lon0 = 36.164131
points_hosp = []
points_pol = []

for i in range(len(df)):
    latitude = df.iloc[i, 22]
    lon = df.iloc[i, 23]
    points_hosp.append(pm.geodetic2enu(latitude, lon, 0, latitude0, lon0, 0))
for k in range(len(points_ru)):
    latitude = points_ru.iloc[k, 5]
    lon = points_ru.iloc[k, 4]
    points_pol.append(pm.geodetic2enu(latitude, lon, 0, latitude0, lon0, 0))

kd_tree1 = KDTree(points_hosp)
kd_tree2 = KDTree(points_pol)
indexes = kd_tree1.query_ball_tree(kd_tree2, r=25000)
indexes_50 = kd_tree1.query_ball_tree(kd_tree2, r=50000)

means = []

for i in range(len(indexes)):
    if len(indexes[i]) != 0:
        a = sum(points_ru.iloc[indexes[i], 7]) / len(indexes[i])
        means.append(a)
    else:
        means.append('-1')

means_2020_25 = means[:]
means = []

for i in range(len(indexes_50)):
    if len(indexes_50[i]) != 0:
        a = sum(points_ru.iloc[indexes_50[i], 7]) / len(indexes_50[i])
        means.append(a)
    else:
        means.append('-1')

means_2020_50 = means[:]

# 2021
        
points = pd.read_csv('PM2_5_NT_2023_GRID_2021.txt', delimiter=';')
points_ru = points.loc[points.ISO2 == 'RU']

points_pol = []

for k in range(len(points_ru)):
    latitude = points_ru.iloc[k, 5]
    lon = points_ru.iloc[k, 4]
    points_pol.append(pm.geodetic2enu(latitude, lon, 0, latitude0, lon0, 0))

indexes = kd_tree1.query_ball_tree(kd_tree2, r=25000)
indexes_50 = kd_tree1.query_ball_tree(kd_tree2, r=50000)

means = []

for i in range(len(indexes)):
    if len(indexes[i]) != 0:
        a = sum(points_ru.iloc[indexes[i], 7]) / len(indexes[i])
        means.append(a)
    else:
        means.append('-1')

means_2021_25 = means[:]
means = []

for i in range(len(indexes_50)):
    if len(indexes_50[i]) != 0:
        a = sum(points_ru.iloc[indexes_50[i], 7]) / len(indexes_50[i])
        means.append(a)
    else:
        means.append('-1')

means_2021_50 = means[:]
pollution_df = pd.DataFrame({'pollution_25': list(map(lambda x: str(x).replace('-1.0', "NaN").replace('-1', "NaN"), [(int(means_2020_25[i]) + int(means_2021_25[i])) / 2 for i in range(len(means_2020_25))])), 'pollution_50': list(map(lambda x: str(x).replace('-1.0', "NaN").replace('-1', "NaN"), [(int(means_2020_50[i]) + int(means_2021_50[i])) / 2 for i in range(len(means_2020_50))]))})
df['key'] = list(zip(df['latitude'], df['longitude']))
df = df.reset_index()
del df['index']

merged_df = df
merged_df['pollution_25'] = pollution_df['pollution_25']
merged_df['pollution_50'] = pollution_df['pollution_50']

original_df['pollution_25'] = None
original_df['pollution_50'] = None

for index, row in original_df.iterrows():
    if index == 0:
        continue
    key = (row['latitude'], row['longitude'])
    
    if row['latitude'] not in [None, "NA", "nan", 'NaN']:
        if (merged_df['key'] == key).any():

            pollution_25_val = merged_df.loc[merged_df['key'] == key, 'pollution_25'].values[0]
            pollution_50_val = merged_df.loc[merged_df['key'] == key, 'pollution_50'].values[0]

            original_df.at[index, 'pollution_25'] = pollution_25_val
            original_df.at[index, 'pollution_50'] = pollution_50_val
        else:
            row['pollution_25'] = 'NaN'
            row['pollution_50'] = 'NaN'

    else:
        row['pollution_25'] = 'NaN'
        row['pollution_50'] = 'NaN'

original_df.to_csv('result.csv', index=False)
