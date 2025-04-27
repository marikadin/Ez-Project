import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

# Define the path to the directory
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
    # Dictionary to hold the sum of absolute E-field values and the count for each hour, grouped by day
    daily_data = defaultdict(lambda: {hour: [] for hour in range(24)})  # Structure: {day: {hour: [values]}}
    i = 0  # To count the number of valid files processed

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".dat"):
            file_path = os.path.join(directory, filename)

            # Open and read the file
            with open(file_path, 'r') as file:
                reader = csv.reader(file)

                # Process each row in the file
                for row in reader:
                    try:
                        timestamp = row[0]  # Assuming timestamp is the first column
                        e_field_avg = float(row[2])  # Assuming E_field_Avg is the third column

                        # Convert timestamp string to a datetime object
                        timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')  # Adjust format as necessary

                        # Format the date as dd/mm/yyyy to check against skip dates
                        formatted_date = timestamp_obj.strftime('%d/%m/%Y')

                        # Skip files with dates in the skip list
                        if formatted_date in dates_to_skip:
                            continue

                        # Extract the day of the week and the hour part of the timestamp
                        day_name = timestamp_obj.strftime('%A')  # Get day name (e.g., 'Monday')
                        hour = timestamp_obj.hour

                        # Take the absolute value of the E-field average
                        e_field_avg_abs = abs(e_field_avg)

                        # Append the value to the appropriate day and hour
                        daily_data[day_name][hour].append(e_field_avg_abs)

                    except ValueError:
                        # Skip rows that might have invalid or missing data
                        continue

            # Increment the counter for valid files
            i += 1

    # Calculate the average for each hour of each day
    print(f'{i} valid files processed')
    hourly_avg_per_day = {}
    for day, hours in daily_data.items():
        hourly_avg_per_day[day] = []
        for hour in range(24):
            values = hours[hour]
            if values:
                hourly_avg_per_day[day].append(sum(values) / len(values))  # Calculate average for the hour
            else:
                hourly_avg_per_day[day].append(0)  # If no data, append 0

    # Plotting
    cmap = plt.cm.get_cmap('tab10')  # Color map for different days
    days_order = [ "Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # Plot the averages for each day of the week
    plt.figure(figsize=(12, 6))
    for idx, day in enumerate(days_order):
        if day in hourly_avg_per_day:  # Only plot days that have data
            color = cmap(idx / 7)
            plt.plot(range(24), hourly_avg_per_day[day], label=day, color=color)

    plt.title('Daily Averages PG value Over Time')
    plt.xlabel('Hour of the Day [LT]')
    plt.ylabel('Average PG Value [V/m]')
    plt.xticks(range(24))
    plt.legend(title="Days of the Week")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Call the function to process the data and plot the graph
process_and_plot_data(directory_path)
