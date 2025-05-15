import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
import pandas as pd
import matplotlib.cm as cm

# ==== CONFIGURATION ====
directory_path = "PG"
excel_file = "data.xlsx"
usecols = [0, 3, 4]
column_names = ['Date', 'NOx', 'PM2.5']
dates_to_skip = {
    "03/11/2024", "04/11/2024", "05/11/2024", "17/11/2024", "18/11/2024",
    "19/11/2024", "20/11/2024", "23/11/2024", "24/11/2024", "25/11/2024",
    "26/11/2024", "27/11/2024", "28/11/2024", "29/11/2024", "19/12/2024",
    "20/12/2024", "21/12/2024", "22/12/2024", "23/12/2024", "24/12/2024",
    "25/12/2024", "26/12/2024", "27/12/2024", "28/12/2024", "29/12/2024",
    "30/12/2024", "31/12/2024", "10/01/2025", "11/01/2025", "12/01/2025",
    "22/01/2025", "23/01/2025", "24/01/2025", "04/02/2025", "05/02/2025",
    "06/02/2025", "08/02/2025", "09/02/2025", "10/02/2025", "11/02/2025",
    "19/02/2025", "20/02/2025", "22/02/2025", "23/02/2025", "28/02/2025",
    "01/03/2025"
}

days_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# ==== PG DATA ====
def process_pg_data(directory):
    daily_data = defaultdict(lambda: {hour: [] for hour in range(24)})
    for filename in os.listdir(directory):
        if filename.endswith(".dat"):
            with open(os.path.join(directory, filename), 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        timestamp = row[0]
                        e_field_avg = float(row[2])
                        timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                        formatted_date = timestamp_obj.strftime('%d/%m/%Y')
                        if formatted_date in dates_to_skip:
                            continue
                        day_name = timestamp_obj.strftime('%A')
                        hour = timestamp_obj.hour
                        e_field_avg_abs = abs(e_field_avg)
                        daily_data[day_name][hour].append(e_field_avg_abs)
                    except:
                        continue
    # Flatten into 168 hour values
    pg_data = []
    for day in days_order:
        for hour in range(24):
            values = daily_data[day][hour]
            avg = sum(values) / len(values) if values else 0
            pg_data.append(avg)
    return pg_data

# ==== EXCEL POLLUTANT DATA ====
def process_pollutant_data(file, usecols, colnames):
    df = pd.read_excel(file, engine='openpyxl', usecols=usecols, skiprows=4)
    df.columns = colnames
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

    pollutants = df.columns[1:]
    avg_results = {}

    for pollutant in pollutants:
        df[pollutant] = pd.to_numeric(df[pollutant], errors='coerce')
        hourly_dict = {day: [[] for _ in range(24)] for day in days_order}
        for idx, row in df.iterrows():
            date = row['Date']
            value = row[pollutant]
            if pd.notna(date) and pd.notna(value):
                day_name = date.day_name()
                hour = date.hour
                if day_name in hourly_dict and 0 <= hour < 24:
                    hourly_dict[day_name][hour].append(value)
        # Compute averages
        flat_data = []
        for day in days_order:
            for hour in range(24):
                vals = hourly_dict[day][hour]
                avg = sum(vals) / len(vals) if vals else 0
                flat_data.append(avg)
        avg_results[pollutant] = flat_data
    return avg_results

# ==== MAIN COMBINED PLOT ====
def plot_combined():
    pg_week = process_pg_data(directory_path)
    pollutant_data = process_pollutant_data(excel_file, usecols, column_names)

    x = list(range(168))
    fig, ax1 = plt.subplots(figsize=(14, 6))

    # PG - Left Axis
    ln1 = ax1.plot(x, pg_week, color='black', label='PG [V/m]', linewidth=2)
    ax1.set_ylabel('PG [V/m]', color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # NOx - Right Axis
    ax2 = ax1.twinx()
    ln2 = ax2.plot(x, pollutant_data['NOx'], color='red', label='NOx [µg/m³]', linewidth=2)
    ax2.set_ylabel('NOx [µg/m³]', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # PM2.5 - Third Axis
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))  # Shift to the right
    ln3 = ax3.plot(x, pollutant_data['PM2.5'], color='blue', label='PM2.5 [µg/m³]', linewidth=2)
    ax3.set_ylabel('PM2.5 [µg/m³]', color='blue')
    ax3.tick_params(axis='y', labelcolor='blue')

    # X-axis settings
    ax1.set_xticks([i * 24 + 12 for i in range(7)])
    ax1.set_xticklabels(days_order)
    ax1.set_xlabel("Day of the Week")
    ax1.set_title("Weekly Comparison of PG, NOx, and PM2.5")
    ax1.grid(True)

    # Extra X-axis: Hour ranges
    # Extra X-axis: Hour of the Week (0–167)
    ax_top = ax1.twiny()
    ax_top.set_xlim(ax1.get_xlim())  # Align with actual plot
    tick_positions = list(range(0, 169, 6))  # Includes 168
    ax_top.set_xticks(tick_positions)
    ax_top.set_xticklabels([str(i) for i in tick_positions])
    ax_top.set_xlabel("Hour of the Week [0–167]")

    # Combined legend
    lines = ln1 + ln2 + ln3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.tight_layout()
    plt.show()

plot_combined()
