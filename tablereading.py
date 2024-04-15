
import pandas as pd

# Define the file paths (assuming you have 8 CSV files)
file_paths = [
    'data1.csv', 'data3.csv'
]

# Define the descriptor you are interested in
descriptor = 'Max'
#fit_column = 'Fit'  # You may adjust the exact fit column name logic below as per your data

# Function to standardize and ensure unique header names based on common prefixes
def standardize_headers(headers):
    standardized = []
    header_count = {}
    for header in headers:
        new_header = header
        
        if header.startswith('Basic Size'):
            new_header = 'Basic Size'
        elif header.startswith('Fit'):
            new_header = 'Fit'
        elif 'Max' in header or 'Min' in header:
            new_header = 'Descriptor'
        if new_header in header_count:
            header_count[new_header] += 1
            new_header = f"{new_header}_{header_count[new_header]}"
        else:
            header_count[new_header] = 0
        
        standardized.append(new_header)
    return standardized

# List to collect the results
results = []

for file_path in file_paths:
    # Read the CSV file without skipping any rows to see all headers
    data = pd.read_csv(file_path)

    # Consolidate headers using forward fill for NaN values and combine into single header
    headers = data.iloc[1:4, :].ffill(axis=0).astype(str).agg(' '.join).str.strip().tolist()
    headers = standardize_headers(headers)  # Standardize headers based on common prefixes

    # Reload the data with the new headers, skipping the initial header rows
    data = pd.read_csv(file_path, header=None, skiprows=4, names=headers)

    # Print columns for debugging
    print("Column names:", data.columns)  # Debugging step to check column names

    # Filter for the specific basic size and descriptor
    filtered_data = data[
        (data['Descriptor'].astype(str) == descriptor)
    ]

    # Extract the specific fit value
    fit_values = filtered_data['Fit'].values if 'Fit' in filtered_data.columns and not filtered_data.empty else "Value not found"

    # Append the result along with file identifier and all fit values found
    results.append((file_path, fit_values))

# Output the results
for result in results:
    print(f"File: {result[0]}, Fit Values: {result[1]}")
