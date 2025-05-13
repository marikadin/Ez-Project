import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Define the path to the directory
directory_path = "Ez Holon"

# Set of dates to skip
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



# Function to process the .dat files and calculate averages per hour
def process_and_plot_data(directory):
    # Dictionary to hold the sum of absolute E-field values and the count for each hour
    hourly_data = defaultdict(lambda: {"sum": 0, "count": 0})
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

                        # Format the date as dd/mm/yyyy to check against dates_to_skip
                        formatted_date = timestamp_obj.strftime('%d/%m/%Y')

                        # Skip files with dates in the skip list
                        if formatted_date in dates_to_skip:
                            continue

                        # Extract the hour part of the timestamp
                        hour = timestamp_obj.hour

                        # Take the absolute value of the E-field average
                        e_field_avg_abs = abs(e_field_avg)

                        # Update sum and count for the given hour
                        hourly_data[hour]["sum"] += e_field_avg_abs
                        hourly_data[hour]["count"] += 1

                    except ValueError:
                        # Skip rows that might have invalid or missing data
                        continue

            # Increment the counter for valid files
            i += 1

    # Calculate the average for each hour
    # Calculate the average for each hour
    print(f'{i} valid files processed')
    hourly_avg = {}
    for hour, data in hourly_data.items():
        if data["count"] > 0:
            hourly_avg[hour] = data["sum"] / data["count"]

    # Plot the results in LT and UT (shifted)
    if hourly_avg:
        hours = sorted(hourly_avg.keys())
        lt_averages = [hourly_avg[hour] for hour in hours]

        # Shift 2 hours back for UT, wrapping around with modulo 24
        ut_hourly_avg = {(hour - 2) % 24: avg for hour, avg in hourly_avg.items()}
        ut_hours = sorted(ut_hourly_avg.keys())
        ut_averages = [ut_hourly_avg[hour] for hour in ut_hours]

        plt.figure(figsize=(10, 6))
        plt.plot(hours, lt_averages, marker='o', linestyle='--', color='b', label='Local Time (LT)')
        plt.plot(ut_hours, ut_averages, marker='s', linestyle='-', color='k', label='Universal Time (UT)')
        plt.title('Average PG values over time')
        plt.xlabel('Time')
        plt.ylabel('Average PG [V/m]')
        plt.xticks(range(0, 24))  # Show all 24 hours
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("No valid data to plot.")


# Call the function to process the data and plot the graph
process_and_plot_data(directory_path)