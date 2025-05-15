import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'weather data.xlsx'
df = pd.read_excel(file_path, sheet_name='data_20171201_20180208', header=1)

# Combine Date and Time into a single datetime column
df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), errors='coerce')

# Clean the data
df_clean = df.dropna(subset=['Datetime', 'Rate'])
df_clean['Rate'] = pd.to_numeric(df_clean['Rate'], errors='coerce')

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df_clean['Datetime'], df_clean['Rate'], color='blue', linewidth=0.7)
plt.title("Rain Rate Over Time")
plt.xlabel("Time")
plt.ylabel("Rain Rate")
plt.grid(True)
plt.tight_layout()
plt.show()
