#%% write a sql query to count the number of fraudulent transactions in the credit_card table
from asyncio import graph

import pandas as pd
import sqlite3
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('kaggle/ev_battery_degradation_v1.csv')
conn = sqlite3.connect(':memory:')
data.to_sql('ev_degrade', conn, index=False, if_exists='replace')


#%% Is there a easy winner to Car Model, which is the best?
sql_query = """
SELECT Car_Model, AVG(SoH_Percent) AS Avg_SoH, Battery_Type
FROM Ev_degrade
GROUP BY  Car_Model
ORDER BY Avg_SoH DESC

"""
car_model_data = pd.read_sql(sql_query, conn)
print(car_model_data)

#%% What are the pros and cons to each battery type
sql_query = """
SELECT Battery_Type, AVG(SoH_Percent) AS Avg_SoH, Vehicle_Age_Months
FROM Ev_degrade
GROUP BY  Battery_Type, Vehicle_Age_Months
ORDER BY Avg_SoH DESC
"""
battery_type_data = pd.read_sql(sql_query, conn)
print(battery_type_data)

graph = alt.Chart(battery_type_data).mark_line(point=True).encode(
    x='Vehicle_Age_Months:Q',
    y='Avg_SoH:Q',
    color='Battery_Type:N',
    tooltip=['Battery_Type', 'Vehicle_Age_Months', 'Avg_SoH']
).properties(
    title='Average State of Health (SoH) Degradation over Vehicle Age by Battery Type',
    width=800,
    height=400
)
graph.show()

#%% Does driving style have anything to do which battery or maybe the people buying certain cars
sql_query = """
SELECT  Vehicle_Age_Months, AVG(SoH_Percent) AS Avg_SoH, Driving_Style
FROM Ev_degrade
GROUP BY  Driving_Style, Vehicle_Age_Months
ORDER BY Avg_SoH DESC
"""
car_model_data = pd.read_sql(sql_query, conn)
print(car_model_data)

chart = alt.Chart(car_model_data).mark_line(point=True).encode(
    x='Vehicle_Age_Months:Q',
    y='Avg_SoH:Q',
    color='Driving_Style:N',
    tooltip=['Driving_Style', 'Vehicle_Age_Months', 'Avg_SoH']
).properties(
    title='Average State of Health (SoH) Degradation over Vehicle Age by Driving Style',
    width=800,
    height=400
)
chart.show()
#%% Does Fast charge ratio have an affect on battery life?
sql_query = """
SELECT  Vehicle_Age_Months, AVG(SoH_Percent) AS Avg_SoH, Fast_Charge_Ratio
FROM Ev_degrade
GROUP BY  Fast_Charge_Ratio, Vehicle_Age_Months
ORDER BY Avg_SoH DESC
"""
car_model_data = pd.read_sql(sql_query, conn)
print(car_model_data)

chart = alt.Chart(car_model_data).mark_line(point=True).encode(
    x='Vehicle_Age_Months:Q',
    y='Avg_SoH:Q',
    color='Fast_Charge_Ratio:N',
    tooltip=['Fast_Charge_Ratio', 'Vehicle_Age_Months', 'Avg_SoH']
).properties(
    title='Average State of Health (SoH) Degradation over Vehicle Age by Fast Charge Ratio',
    width=800,
    height=400
)
chart.show()

# %%
