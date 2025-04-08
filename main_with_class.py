import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.cm as cm


class Graphs_24():

    def __init__(self):
        self.usecols = []
        self.file = ""
        self.columns_names = []
        self.averages ={}


    def organizeList_24hours(self, data, dicti, field):
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

    def average_per_hours(self, dicti, listi, field):
        sum = 0
        for i in range(24):
            for j in dicti[field][i]:
                sum += j
            listi[i] = sum / len(dicti[field][i])
            sum = 0

    def Execute(self):
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
            self.organizeList_24hours(df[i].values.tolist(), dicti, i)

        for i in dicti.keys():
            self.average_per_hours(dicti, self.averages[i], i)

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


obj = Graphs_24()
obj.usecols = [0,3,4]
obj.columns_names =['Date', 'NOx','PM2.5']
obj.file = "data.xlsx"
obj.Execute()