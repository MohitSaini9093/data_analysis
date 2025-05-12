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
        if column_name not in self.data.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the data")
            
        # Get the data type of the column
        dtype = self.data[column_name].dtype
        
        # Handle numeric columns
        if pd.api.types.is_numeric_dtype(self.data[column_name]):
            describe = {
                "count": float(self.data[column_name].count()),
                "mean": float(self.data[column_name].mean()),
                "std": float(self.data[column_name].std()),
                "min": float(self.data[column_name].min()),
                "25%": float(self.data[column_name].quantile(0.25)),
                "50%": float(self.data[column_name].median()),
                "75%": float(self.data[column_name].quantile(0.75)),
                "max": float(self.data[column_name].max())
            }
        # Handle object/string columns
        elif pd.api.types.is_object_dtype(self.data[column_name]):
            value_counts = self.data[column_name].value_counts()
            print("Most common values:")
            print(value_counts.index[0])
            describe = {
                "count": float(self.data[column_name].count()),
                "no of unique value": float(self.data[column_name].nunique()),
                "mmost common value": value_counts.index[0],
                "least common value": value_counts.index[-1],
                "missing_values": float(self.data[column_name].isna().sum()),
                "most common value count": float(value_counts.max()),
                "least common value count": float(value_counts.min())
                
                
            }
        # Handle datetime columns
        elif pd.api.types.is_datetime64_dtype(self.data[column_name]):
            describe = {
                "count": float(self.data[column_name].count()),
                "min_date": str(self.data[column_name].min()),
                "max_date": str(self.data[column_name].max()),
                "missing_values": float(self.data[column_name].isna().sum()),
                "unique_dates": float(self.data[column_name].nunique())
            }
        # Handle boolean columns
        elif pd.api.types.is_bool_dtype(self.data[column_name]):
            value_counts = self.data[column_name].value_counts()
            describe = {
                "count": float(self.data[column_name].count()),
                "true_count": float(value_counts.get(True, 0)),
                "false_count": float(value_counts.get(False, 0)),
                "missing_values": float(self.data[column_name].isna().sum())
            }
        else:
            describe = {
                "count": float(self.data[column_name].count()),
                "dtype": str(dtype),
                "missing_values": float(self.data[column_name].isna().sum())
            }
            
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

    def cleanup(self):
        """Clear all data and free memory"""
        if hasattr(self, 'data'):
            del self.data
        # Force garbage collection
        '''import gc
        gc.collect()'''

    def __del__(self):
        """Destructor to ensure cleanup when object is deleted"""
        self.cleanup()

    
    