import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Define the path to the directory
directory_path = "Ez Holon"


# Function to process the .dat files and calculate averages per hour
def process_and_plot_data(directory):
    # Dictionary to hold the sum of absolute E-field values and the count for each hour
    hourly_data = defaultdict(lambda: {"sum": 0, "count": 0})
    i=0
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".dat"):
            i+=1
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

    # Calculate the average for each hour
    print(i, 'hours of samples')
    hourly_avg = {}
    for hour, data in hourly_data.items():
        if data["count"] > 0:
            hourly_avg[hour] = data["sum"] / data["count"]

    # Plot the results
    hours = sorted(hourly_avg.keys())
    averages = [hourly_avg[hour] for hour in hours]

    plt.figure(figsize=(10, 6))
    plt.plot(hours, averages, marker='o', linestyle='-', color='b')
    plt.title('Average Absolute E-field Values per Hour')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Absolute E-field Value')
    plt.xticks(hours)  # Ensure all hours are labeled on the x-axis
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Call the function to process the data and plot the graph
process_and_plot_data(directory_path)
