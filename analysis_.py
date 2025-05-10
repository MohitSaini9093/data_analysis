import pandas as pd
import matplotlib.pyplot as plt
class Analysis:
    def __init__(self, data):
        self.data = data

    def calculate_statistics(self):
        stats = self.data.describe().T[['mean', 'std']]
        return stats

    def filter_data(self, column_name,threshold):
        if not isinstance(threshold, (int, float)):
            raise ValueError("Threshold must be a number")
        filtered_data = self.data[self.data[column_name] > threshold]
        return filtered_data
    def save_to_csv(self, filename):
        if not filename.endswith('.csv'):
            raise ValueError("Filename must end with .csv")
        self.data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    def head_(self, n=5):
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n must be a positive integer")
        return self.data.head(n)
    def tail_(self, n=5):
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n must be a positive integer")
        return self.data.tail(n)
    def info_column(self,column_name):
        return self.data[column_name].info()
    def describe_column(self,column_name):
        describe={"count": self.data[column_name].count(),
                 "mean": self.data[column_name].mean(),
                 "std": self.data[column_name].std(),
                 "min": self.data[column_name].min(),
                 "25%": self.data[column_name].quantile(0.25),
                 "50%": self.data[column_name].median(),
                 "75%": self.data[column_name].quantile(0.75),
                 "max": self.data[column_name].max()}
        return describe
    def group_by(self, column):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' does not exist in the data")
        grouped_data = self.data.groupby(column).mean()
        return grouped_data.reset_index()
    def plot_data(self, x, y):
        if x not in self.data.columns or y not in self.data.columns:
            raise ValueError(f"Columns '{x}' or '{y}' do not exist in the data")
        
        plt.scatter(self.data[x], self.data[y])
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f'Scatter plot of {x} vs {y}')
        plt.show()
    def save_to_excel(self, filename):
        if not filename.endswith('.xlsx'):
            raise ValueError("Filename must end with .xlsx")
        self.data.to_excel(filename, index=False)
        print(f"Data saved to {filename}")  
    def save_to_json(self, filename):
        if not filename.endswith('.json'):
            raise ValueError("Filename must end with .json")
        self.data.to_json(filename, orient='records', lines=True)
        print(f"Data saved to {filename}")
    def save_to_html(self, filename):
        if not filename.endswith('.html'):
            raise ValueError("Filename must end with .html")
        self.data.to_html(filename, index=False)
        print(f"Data saved to {filename}")
    def acending(self, column):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' does not exist in the data")
        sorted_data = self.data.sort_values(by=column, ascending=True)
        return sorted_data.reset_index(drop=True)
    def descending(self, column):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' does not exist in the data")
        sorted_data = self.data.sort_values(by=column, ascending=False)
        return sorted_data.reset_index(drop=True)
    def drop_column(self, column):
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' does not exist in the data")
        self.data = self.data.drop(columns=[column])
        return self.data
    def rename_column(self, old_name, new_name):
        if old_name not in self.data.columns:
            raise ValueError(f"Column '{old_name}' does not exist in the data")
        self.data = self.data.rename(columns={old_name: new_name})
        return self.data

    
    