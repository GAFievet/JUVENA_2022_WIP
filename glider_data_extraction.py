from daily_data_compiling import compiling
import pandas as pd
from datetime_formating import combine_date_time

df=compiling(r'C:\Users\G to the A\PycharmProjects\Paper\glider')

# def extract_glider_data(df):
data=[df['Longitude'].tolist(),df['Latitude'].tolist(),df['GPS_date'].tolist(),df['GPS_time'].tolist()]
print(type(data[2][0]))
print(type(data[3][0]))
