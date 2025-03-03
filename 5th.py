import pandas as pd

def filter_phone_numbers(input_file, output_file):
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return
    
    # Remove leading/trailing spaces from column names and ensure "Phone Number" is a string
    df.columns = df.columns.str.strip()
    if "Phone Number" in df.columns:
        df["Phone Number"] = df["Phone Number"].astype(str).str.strip()
    else:
        print("Column 'Phone Number' not found in the CSV.")
        return

    # Define a set of invalid phone number entries (case-insensitive)
    invalid_entries = {"N/A", "NA", "", "NULL"}
    
    # Filter out rows where the "Phone Number" column has invalid values
    df_filtered = df[~df["Phone Number"].str.upper().isin(invalid_entries)]
    
    # Save the filtered DataFrame to a new CSV file
    try:
        df_filtered.to_csv(output_file, index=False)
        print(f"Filtered CSV saved as: {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    input_file = 'output_data.csv'
    output_file = 'filtered_phone_numbers.csv'
    filter_phone_numbers(input_file, output_file)
