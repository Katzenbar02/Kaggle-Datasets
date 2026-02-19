#%% write a sql query to count the number of fraudulent transactions in the credit_card table
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
SELECT AVG(SoH_Percent) AS Avg_SoH, Driving_Style
FROM Ev_degrade
GROUP BY  Driving_Style
ORDER BY Avg_SoH DESC
"""
car_model_data = pd.read_sql(sql_query, conn)
print(car_model_data)

#%% What are the pros and cons to each battery type

#%% Does driving style have anything to do which battery or maybe the people buying certain cars

#%% Does Fast charge ratio have an affect on battery life?