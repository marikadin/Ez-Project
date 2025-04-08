import pandas as pd
import matplotlib.pyplot as plt
import math


def organizeList_24hours(data, dicti, field):
    index = 0
    for i, value in enumerate(data):
        # Check if the value is a valid number (not NaN)
        if isinstance(value, (int, float)) and not math.isnan(value):
            dicti[field][index].append(value)

        # Update index every 13 values, reset after 23
        if i % 13 != 0:
            pass  # Continue the loop
        else:
            index += 1  # Move to the next hour (index)

        # Ensure the index wraps around after 23 hours (24-hour cycle)
        if index == 24:
            index = 0
    return dicti


def average_per_hours(dicti, listi, field):
    sum = 0
    for i in range(24):
        for j in dicti[field][i]:
            sum += j
        listi[i] = sum / len(dicti[field][i])
        sum=0


# Read the Excel file, skip the first three rows, and use only columns A, D, and E
df = pd.read_excel('data.xlsx', engine='openpyxl', usecols=[0, 3, 4], skiprows=4)

# Rename columns to appropriate headers
df.columns = ['Date', 'NOx', 'PM2.5']

# Print first few rows to debug and check the 'Date' column
# Convert 'Date' column to datetime, ensuring invalid data is coerced to NaT
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

# Convert the 'NOx' and 'PM2.5' columns to numeric, invalid entries will become NaN
df['NOx'] = pd.to_numeric(df['NOx'], errors='coerce')
df['PM2.5'] = pd.to_numeric(df['PM2.5'], errors='coerce')

# Convert the columns to lists
NOx = df['NOx'].values.tolist()
PM = df['PM2.5'].values.tolist()

# Initialize the dictionary with empty lists for each hour
dicti = {"NOx": [[] for _ in range(24)], "PM2.5": [[] for _ in range(24)]}

# Organize the data into hourly lists for NOx and PM2.5
organizeList_24hours(PM, dicti, 'PM2.5')
organizeList_24hours(NOx, dicti, 'NOx')

# Initialize lists to store the hourly averages
finale_NOx = [None for _ in range(24)]
finale_PM = [None for _ in range(24)]

# Calculate the average per hour for both NOx and PM2.5
average_per_hours(dicti, finale_PM, "PM2.5")
average_per_hours(dicti, finale_NOx, "NOx")

# Print the results
print("Hourly averages for NOx:", finale_NOx)
print("Hourly averages for PM2.5:", finale_PM)

# Plotting the results for visualization
plt.figure(figsize=(10, 6))
plt.plot(range(24), finale_NOx, label='NOx', marker='o', linestyle='-', color='red')
plt.plot(range(24), finale_PM, label='PM2.5', marker='o', linestyle='-', color='blue')
plt.title('Hourly Averages of NOx and PM2.5')
plt.xlabel('Hour of the Day')
plt.ylabel('Average Value')
plt.xticks(range(24))  # Set x-axis labels as hours
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
