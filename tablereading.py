
import pandas as pd

# Define file paths for "hole" basis and "shaft" basis data sets
hole_files = ['Hole1.csv', 'Hole2.csv', 'Hole3.csv', 'Hole4.csv' ]  # Adjust paths as necessary
shaft_files = ['shaft1.csv', 'shaft2.csv', 'shaft3.csv', 'shaft4.csv']  # Adjust paths as necessary


def load_files(file_list):
    combined_data = pd.DataFrame()
    for file_path in file_list:
        print(f"Loading file: {file_path}")
        data = pd.read_csv(file_path, header=[0, 1])
        
        # Fix the headers by removing any 'Unnamed' labels and ensuring proper labeling
        data.columns = pd.MultiIndex.from_tuples([(x if 'Unnamed' not in x[0] else y, x[1])
                                                  for x, y in zip(data.columns, ['Basic Size', 'Max/Min'] + [x[0] for x in data.columns[2:]][::3] * 3)])
        
        print("Columns after renaming:", data.columns[2])
        
        # Set the first two columns ('Basic Size', 'Max/Min') as the multi-index
        data.set_index(('Basic Size', 'MaxMin'), inplace=True)
        
        # Combine the data from each file
        combined_data = pd.concat([combined_data, data], axis=0)


    return combined_data

# Example file paths
hole_data = load_files(hole_files)
print(hole_data.head())

# Function to retrieve Min and Max values based on user inputs
def get_min_max_values(data, descriptor, hole_or_shaft, basic_size):
    # Filter data based on Basic Size and convert to numeric as needed
    basic_size_data = data.xs(basic_size, level='Basic Size', axis=1, drop_level=False)
    try:
        specific_data = basic_size_data.xs(descriptor, level='Descriptor', axis=1).xs(hole_or_shaft, level='Hole/Shaft', axis=1)
        min_value = pd.to_numeric(specific_data.loc['Min'], errors='coerce').min()
        max_value = pd.to_numeric(specific_data.loc['Max'], errors='coerce').max()
        return min_value, max_value
    except KeyError:
        return "Data not found", "Data not found"

# Example usage
descriptor = "Loose Running C11/h11"  # or any other descriptor as per user's choice
hole_or_shaft = "Hole"  # or "Shaft" depending on the user's choice
basic_size = '30'  # example basic size

# Choose the correct data set based on whether we are considering the hole or shaft as constant
if hole_or_shaft == "Hole":
    min_val, max_val = get_min_max_values(hole_data, descriptor, hole_or_shaft, basic_size)
else:
    min_val, max_val = get_min_max_values(shaft_data, descriptor, hole_or_shaft, basic_size)

print(f"Min Fit: {min_val}, Max Fit: {max_val}")
