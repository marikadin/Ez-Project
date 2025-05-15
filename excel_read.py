import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the Excel file
file_path = 'weather data.xlsx'
df = pd.read_excel(file_path, sheet_name='data_20171201_20180208', header=1)

# Drop rows with missing time or rate
df = df.dropna(subset=['Time', 'Rate'])

# Convert columns to proper formats
df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')

# Drop any rows that failed conversion
df = df.dropna(subset=['Time', 'Rate'])

# Assign all times to a dummy date (needed for Matplotlib time plotting)
df['TimeOnly'] = df['Time'].apply(lambda t: t.replace(year=2000, month=1, day=1))

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df['TimeOnly'], df['Rate'], color='blue', linewidth=0.7)

# Format x-axis to show time in HH:MM format

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # every hour
plt.gcf().autofmt_xdate()

plt.title("Rain Rate vs Time of Day (24-Hour Format)")
plt.xlabel("Time of Day")
plt.ylabel("Rain Rate")
plt.grid(True)
plt.tight_layout()
plt.show()
