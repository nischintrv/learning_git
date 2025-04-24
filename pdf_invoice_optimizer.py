import pandas as pd
from datetime import datetime
import ollama
import time
from fpdf import FPDF
def load_and_prep_data(file_path):
    print("Loading merged data...")
    df = pd.read_csv(file_path)
    df['Received Date'] = pd.to_datetime(df['Received Date'], format='%d-%m-%Y', errors='coerce')
    df['Processed Date'] = pd.to_datetime(df['Processed Date'], format='%d-%m-%Y', errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    current_date = datetime(2025, 3, 12)
    df['Days_Taken'] = df.apply(
        lambda row: (row['Processed Date'] - row['Received Date']).days
        if pd.notna(row['Processed Date'])
        else (current_date - row['Received Date']).days, axis=1
    )
    required_cols = ['Invoice_no', 'Received Date', 'Processed Date', 'Amount', 'Assigned To', 
                    'Date', 'Transaction Number', 'Debit', 'Credit', 'Balance']
    assert all(col in df.columns for col in required_cols), "Missing required columns"
    assert df[required_cols].notnull().all().all(), "Missing values in required columns"
    data_text = df.to_string(index=False)
    print("Data prepared successfully!")
    return data_text, df
def analyze_with_llama(data_text):
    print("Analyzing with LLaMA...")
    prompt = f"""
    You’re an efficiency expert for financial accounting. Here’s invoice data:
    {data_text[:10000]}
    Suggest improvements for:
    - Delays: Days_Taken > 5 days (pending or processed).
    - Workload: Uneven distribution among Assigned_To (e.g., acctnt_1 to acctnt_6).
    Be concise, list specific Invoice_no where applicable, and focus on actionable steps.
    """
    try:
        response = ollama.chat(model='llama3.1:8b', messages=[{'role': 'user', 'content': prompt}])
        print("Analysis complete!")
        return response['message']['content']
    except Exception as e:
        print(f"Error during LLaMA analysis: {e}")
        return None
if __name__ == "__main__":
    file_path = r"D:\Think Solution\gl_ic.csv"
    data_text, df = load_and_prep_data(file_path)
    
    sample_df = df.head(100)
    print("\nSample Workload Counts:")
    print(sample_df['Assigned To'].value_counts())
    print("\nSample Delayed Invoices (Days_Taken > 5):")
    print(sample_df[sample_df['Days_Taken'] > 5][['Invoice_no', 'Days_Taken', 'Assigned To']])
    
    print("\nInvoiceOptimizer Suggestions:")
    suggestions = analyze_with_llama(data_text)
    if suggestions:
        print(suggestions)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Invoice Optimization Suggestions", ln=True, align="C")
        pdf.multi_cell(0, 10, suggestions)
        pdf_file = f"D:\Think Solution\suggestions_{timestamp}.pdf"
        pdf.output(pdf_file)
        print(f"Suggestions saved to 'suggestions_{timestamp}.pdf'")
 