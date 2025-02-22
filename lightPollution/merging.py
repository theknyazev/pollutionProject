import pandas as pd

years = [2017, 2018, 2019, 2020, 2021]

merged_df = pd.DataFrame()

for year in years:
    df = pd.read_csv(f'output_{year}.csv')
    df = df[['Latitude', 'Longitude', 'Brightness']].rename(columns={'Brightness': str(year)})
    if merged_df.empty:
        merged_df = df
    else:
        merged_df = pd.merge(merged_df, df, on=['Latitude', 'Longitude'], how='outer')

merged_df['average'] = merged_df[years].mean(axis=1)

year_columns = [str(year) for year in years]
export_columns = ['Latitude', 'Longitude'] + year_columns + ['average']

merged_df.to_csv('pollution_data.csv', index=False, columns=export_columns)
