#%% write a sql query to count the number of fraudulent transactions in the credit_card table
import pandas as pd
import sqlite3
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('kaggle/ev_battery_degradation_v1.csv')
conn = sqlite3.connect(':memory:')
data.to_sql('ev_degrade', conn, index=False, if_exists='replace')

#%%
sql_query = """\
SELECT *
FROM ev_degrade
"""
# %%
print(pd.read_sql(sql_query, conn).describe())

# %%
# Analyse how soH_Percent degrade over Vehicle_age_Months for differnt Battery_tpes
sql_query1 = """
SELECT Battery_Type, Vehicle_age_Months AS Age_Months, AVG(SoH_Percent) AS Avg_SoH
FROM ev_degrade
GROUP BY Battery_Type, Age_Months
ORDER BY Battery_Type, Age_Months
"""
# %%
degrade_data = pd.read_sql(sql_query1, conn)
# %%
chart = alt.Chart(degrade_data).mark_line(point=True).encode(
    x='Age_Months:Q',
    y='Avg_SoH:Q',
    color='Battery_Type:N',
    tooltip=['Battery_Type', 'Age_Months', 'Avg_SoH']
).properties(
    title='Average State of Health (SoH) Degradation over Vehicle Age by Battery Type',
    width=800,
    height=400
)
chart.show()

#%% what is the average decrease in SoH_Percent for each Battery_Type every month
sql_query2 = """
SELECT Battery_Type, AVG(SoH_Percent) AS Avg_SoH, AVG(Vehicle_age_Months) AS Avg_Age_Months
FROM ev_degrade
GROUP BY Battery_Type
"""
degrade_summary = pd.read_sql(sql_query2, conn)
degrade_summary['Avg_Decrease_Per_Month'] = degrade_summary['Avg_SoH'] / degrade_summary['Avg_Age_Months']
print(degrade_summary[['Battery_Type', 'Avg_Decrease_Per_Month']])

#%% what is the distribution of SoH_Percent for each Battery_Type
sql_query3 = """
SELECT Battery_Type, SoH_Percent
FROM ev_degrade
"""
soh_data = pd.read_sql(sql_query3, conn)
plt.figure(figsize=(10, 6))
sns.boxplot(x='Battery_Type', y='SoH_Percent', data=soh_data)
plt.title('Distribution of State of Health (SoH) Percent by Battery Type')
plt.xlabel('Battery Type')
plt.ylabel('State of Health (SoH) Percent')
plt.show()









# %%
#  Heatmap of the ev_degradation data to see the correlation between the different features remove the non numeric features
numeric_data = data.select_dtypes(include=['float64', 'int64'])
correlation_matrix = numeric_data.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap of EV Degradation Data')
plt.show()



# %%
