import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

directory_path = "Ez Holon"

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

def process_and_plot_data(directory):
    daily_data = defaultdict(lambda: {hour: [] for hour in range(24)})
    i = 0

    for filename in os.listdir(directory):
        if filename.endswith(".dat"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
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
                    except ValueError:
                        continue
            i += 1

    print(f'{i} valid files processed')

    days_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    full_week_data = []

    for day in days_order:
        for hour in range(24):
            values = daily_data[day][hour]
            avg = sum(values) / len(values) if values else 0
            full_week_data.append(avg)

    # Plotting
    fig, ax1 = plt.subplots(figsize=(14, 6))
    cmap = plt.cm.get_cmap('tab10')

    for i in range(7):
        start = i * 24
        end = (i + 1) * 24
        if i > 0:
            start -= 1
        ax1.plot(range(start, end), full_week_data[start:end], color=cmap(i), label=days_order[i])

    # Primary x-axis: day names at midpoint
    ax1.set_xticks([i * 24 + 12 for i in range(7)])
    ax1.set_xticklabels(days_order)
    ax1.set_xlabel("Day of the Week")
    ax1.set_ylabel("Average PG Value [V/m]")
    ax1.set_title("Average PG Value Over the Week (Continuous Line, Day-Colored)")
    ax1.grid(True)
    ax1.legend(title="Days")

    # Secondary x-axis: hour ranges (0-24, 24-48, ...)
    ax2 = ax1.twiny()
    hour_positions = list(range(0, 168 + 1, 24))  # 0 to 168 hours, every 24
    hour_labels = [f"{h}-{h+24}" for h in hour_positions[:-1]]
    ax2.set_xticks([h + 12 for h in hour_positions[:-1]])  # center align labels
    ax2.set_xticklabels(hour_labels)
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xlabel("Hour Range")

    plt.tight_layout()
    plt.show()

process_and_plot_data(directory_path)
