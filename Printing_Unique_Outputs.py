import pandas as pd
import numpy as np
# printing unique output values from the dataset
def print_unique_outputs():
    data_path = r"resources\data\Extended_Fruits_Dataset2.csv"
    df = pd.read_csv(data_path)
    unique_outputs = df['Output'].unique()
    print("Unique output values in the dataset:")
    for fruit in unique_outputs:
        print(fruit)

# Call the function to print unique outputs
print_unique_outputs()
