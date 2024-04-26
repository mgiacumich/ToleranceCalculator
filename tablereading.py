import pandas as pd
import numpy as np


def load_csv(csv_paths):
    all_dfs = []  # List to store each DataFrame loaded from the CSVs
    for csv_path in csv_paths:
        df = pd.read_csv(csv_path, header=[0, 1])
        header = df.columns.to_flat_index().str.join('_').str.strip('_')
        df.columns = header
        df = df.iloc[2:].reset_index(drop=True)
        df.rename(columns={header[0]: 'Basic Size', header[1]: 'Max/Min'}, inplace=True)
        df.set_index(['Basic Size', 'Max/Min'], inplace=True)
        
        # Convert strings with comma decimals to floats
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].str.replace(',', '.').astype(float)
        
        all_dfs.append(df)
    #return all_dfs
    combined_df = pd.concat(all_dfs)
    #print(combined_df)
    return combined_df
    

def convert_index_to_float(df):
    # Ensure the 'Basic Size' index is a float for proper indexing
    df.index = df.index.set_levels(df.index.levels[0].astype(float), level=0)
    return df

def get_min_max_values(df, category, fit, basic_size):
    # Convert the basic_size to a float and construct the column prefix
    basic_size = float(basic_size)
    prefix = f"{category}_{fit}"
    
    # Query the DataFrame for Min and Max values
    min_val = df.loc[(basic_size, 'Min'), df.columns.str.startswith(prefix)].values[0]
    max_val = df.loc[(basic_size, 'Max'), df.columns.str.startswith(prefix)].values[0]
    return min_val, max_val

def find_nearest_greater_size(df, basic_size):
    # Get all available sizes and find the closest larger size
    available_sizes = df.index.levels[0].values
    larger_sizes = available_sizes[available_sizes > basic_size]
    if larger_sizes.size > 0:
        nearest_size = np.min(larger_sizes)
        print(f"Value rounded up to {nearest_size}")
        return nearest_size
    else:
        raise ValueError("No larger size available.")

# File paths for the CSV data
hole_csv_paths = ['Hole1.csv', 'Hole2.csv', 'Hole3.csv', 'Hole4.csv']
shaft_csv_paths = ['Shaft1.csv', 'Shaft2.csv', 'Shaft3.csv', 'Shaft4.csv']

# Load and clean the CSV files
hole_df_cleaned = load_csv(hole_csv_paths)
shaft_df_cleaned = load_csv(shaft_csv_paths)

# Convert the 'Basic Size' index to float for both DataFrames
hole_df_cleaned_float_index = convert_index_to_float(hole_df_cleaned)
shaft_df_cleaned_float_index = convert_index_to_float(shaft_df_cleaned)

# Define query parameters
category = 'Loose Running H11/cll'  # Category to query, such as fit type
basic_size = 1.8  # Basic size as a float
hole_or_shaft = 'Shaft'  # Define whether to query 'Hole' or 'Shaft'
fit = 'Fit'

# Choose the correct DataFrame based on 'Hole' or 'Shaft'
df_to_query = hole_df_cleaned_float_index if hole_or_shaft == 'Hole' else shaft_df_cleaned_float_index

if basic_size not in df_to_query.index.levels[0]:
    basic_size = find_nearest_greater_size(df_to_query, basic_size)

# Get the min and max values for the specified basic size and category
min_val, max_val = get_min_max_values(df_to_query, category, fit, basic_size)
print(f"{hole_or_shaft} - Basic Size {basic_size}, Category {category}: Min Value = {min_val}, Max Value = {max_val}")