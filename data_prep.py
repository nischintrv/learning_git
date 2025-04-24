import pandas as pd
from datetime import datetime
 
def load_and_prep_data(file_path):
    print("Loading merged data...")
    # Load the merged CSV
    df = pd.read_csv(file_path)
   
    # Clean and standardize dates
    df['Received Date'] = pd.to_datetime(df['Received Date'], format='%d-%m-%Y', errors='coerce')
    df['Processed Date'] = pd.to_datetime(df['Processed Date'], format='%d-%m-%Y', errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
   
    # Current date (March 12, 2025)
    current_date = datetime(2025, 3, 12)
   
    # Calculate Days_Taken
    df['Days_Taken'] = df.apply(
        lambda row: (row['Processed Date'] - row['Received Date']).days
        if pd.notna(row['Processed Date'])
        else (current_date - row['Received Date']).days, axis=1
    )
   
    # Validate key columns
    required_cols = ['Invoice_no', 'Received Date', 'Processed Date', 'Amount', 'Assigned To',
                    'Date', 'Transaction Number', 'Debit', 'Credit', 'Balance']
    assert all(col in df.columns for col in required_cols), "Missing required columns"
    assert df[required_cols].notnull().all().all(), "Missing values in required columns"
   
    # Convert to text for LLaMA
    data_text = df.to_string(index=False)
    print("Data prepared successfully!")
    return data_text, df
 
if __name__ == "__main__":
    # Replace with your file path
    file_path = r"D:\Think Solution\gl_ic.csv"
    data_text, df = load_and_prep_data(file_path)
   
    # Print sample for verification
    print("\nSample of prepared data:")
    print(data_text[:1000])  # First 1000 characters
   
    # Save cleaned DataFrame for reference (optional)
    df.to_csv(r'D:\Think Solution\cleaned_merged_data.csv', index=False)
    print("Cleaned data saved to 'cleaned_merged_data.csv'")