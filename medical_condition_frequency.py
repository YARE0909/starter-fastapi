import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

def plot_categorical_frequency(file_path, column_name):
    # Load the CSV file into a DataFrame
    patients_data = pd.read_csv(file_path)

    # Plotting Categorical Frequency
    counts = patients_data[column_name].value_counts()


    # Format data
    data_array = [
        {"name": category, "count": count.item()}  # Use item() to convert numpy.int64 to standard int
        for category, count in zip(counts.index, counts.values)
    ]

    print(data_array)

    return data_array
