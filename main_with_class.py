import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.cm as cm


class Graphs_24():

    def __init__(self):
        self.usecols = []
        self.file = ""
        self.columns_names = []
        self.averages = {}

    def organizeList_24hours(self, df, dicti, field):
        for idx, row in df.iterrows():
            date = row['Date']
            value = row[field]
            if pd.notna(date) and pd.notna(value):
                hour = date.hour
                if 0 <= hour < 24:
                    dicti[field][hour].append(value)

    def average_per_hours(self, dicti, listi, field):
        sum = 0
        for i in range(24):
            for j in dicti[field][i]:
                sum += j
            listi[i] = sum / len(dicti[field][i]) if len(dicti[field][i]) > 0 else 0
            sum = 0

    def plot(self):
        df = pd.read_excel(self.file, engine='openpyxl', usecols=self.usecols, skiprows=4)

        # Rename columns to appropriate headers
        df.columns = self.columns_names

        # Print first few rows to debug and check the 'Date' column
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
        dicti = {}
        for i in df.columns[1:]:
            df[i] = pd.to_numeric(df[i], errors='coerce')
            dicti[i] = [[] for _ in range(24)]
            self.averages[i] = [[] for _ in range(24)]

        for i in dicti.keys():
            self.organizeList_24hours(df, dicti, i)

        for i in dicti.keys():
            self.average_per_hours(dicti, self.averages[i], i)

        # Print the 24-hour averages to the terminal
        print("24-Hour Averages:")
        for pollutant in dicti.keys():
            print(f"\n{pollutant}:")
            for hour in range(24):
                print(f"Hour {hour}: {self.averages[pollutant][hour]:.2f}")

        cmap = cm.get_cmap('tab10')

        plt.figure(figsize=(10, 6))
        for idx, i in enumerate(dicti.keys()):
            color = cmap(idx / len(dicti))  # Normalize the index for the colormap
            plt.plot(range(24), self.averages[i], label=i, marker='o', linestyle='--', color=color)

        plt.title('Hourly Averages of NOx and PM2.5')
        plt.xlabel('Time[UT]')
        plt.ylabel('Average Value')
        plt.xticks(range(24))  # Set x-axis labels as hours
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


class Graphs_weeks:

    def __init__(self):
        self.usecols = []
        self.file = ""
        self.columns_names = []
        self.averages = {}

    def organize_days(self, df, dicti, col_name):
        for idx, row in df.iterrows():
            date = row['Date']
            value = row[col_name]
            if pd.notna(date) and pd.notna(value):
                day_name = date.day_name()
                hour = date.hour
                if 0 <= hour < 24:
                    dicti[day_name][hour].append(value)

    def average_per_hours(self, daily_dict, result_dict):
        for day in daily_dict:
            result_dict[day] = []
            for hour_values in daily_dict[day]:
                if hour_values:
                    avg = sum(hour_values) / len(hour_values)
                    result_dict[day].append(avg)
                else:
                    result_dict[day].append(0)

    def plot(self):
        df = pd.read_excel(self.file, engine='openpyxl', usecols=self.usecols, skiprows=4)

        # Rename columns
        df.columns = self.columns_names
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

        pollutants = df.columns[1:]  # exclude 'Date'
        for pollutant in pollutants:
            df[pollutant] = pd.to_numeric(df[pollutant], errors='coerce')
            # Dict structure: pollutant -> day -> list of 24 lists (one per hour)
            self.averages[pollutant] = {
                day: [ [] for _ in range(24) ] for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            }

        # Fill in data
        for pollutant in pollutants:
            self.organize_days(df, self.averages[pollutant], pollutant)

        # Compute averages
        avg_results = {}
        for pollutant in pollutants:
            avg_results[pollutant] = {}
            self.average_per_hours(self.averages[pollutant], avg_results[pollutant])

        # Plot
        cmap = cm.get_cmap('tab10')
        days_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        for pollutant in pollutants:
            plt.figure(figsize=(12, 6))
            for idx, day in enumerate(days_order):
                color = cmap(idx / 7)
                plt.plot(range(24), avg_results[pollutant][day], label=day, color=color)

            plt.title(f'Hourly Averages of {pollutant}')
            plt.xlabel('Time [UT]')
            plt.ylabel('Average Value')
            plt.xticks(range(24))
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()

obj = Graphs_24()
obj.usecols = [0,3,4]
obj.columns_names =['Date', 'NOx','PM2.5']
obj.file = "data.xlsx"
obj.plot()
g = Graphs_weeks()
g.file = "data.xlsx"
g.usecols = [0,3,4]  # example columns like ['Date', 'NOx', 'PM2.5']
g.columns_names = ['Date', 'NOx', 'PM2.5']
g.plot()
