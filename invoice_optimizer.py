import pandas as pd
from datetime import datetime
import ollama
import time

def load_and_prep_data(file_path):
    print("Loading merged data...")
    df=pd.read_csv(file_path)
    df['Received Date']=pd.to_datetime(df['Received Date'],format='%d-%m-%Y',errors='coerce')
    df['Processed Date']=pd.to_datetime(df['Processed Date'],format='%d-%m-%Y',errors='coerce')
    df['Date']=pd.to_datetime(df['Date'],format='%d-%m-%Y',errors='coerce')
    current_date=datetime(2025,3,12)
    df['Days_Taken']=df.apply(
        lambda row:(row['Processed Date']-row['Received Date']).days
        if pd.notna(row['Processed Date'])
        else(current_date-row['Received Date']).days,axis=1
    )
    required_cols=['Invoice_no','Received Date','Processed Date','Amount','Assigned To','Date','Transaction Number','Debit','Credit','Balance']
    assert all(col in df.columns for col in required_cols),"Missing required columns"
    assert df[required_cols].notnull().all().all(),"Missing values in required columns"
    data_text=df.to_string(index=False)
    print("Data prepared successfully!")
    return data_text,df

def analyze_with_llama(data_text):
    print("Analyzing with llaMA...")
    prompt=f"""
    You're an efficiencyexpert for financial accounting. Here's invoice data:
    {data_text[:10000]}
    suggest improvements for:
    - Delays: Days_Taken > 5 days (pending or processed).
    - Workload: Uneven distribution among Assigned_To (e.g., acctnt_1 to acctnt_6).
    Be concise,list specific Invoice_no where applicable, and focus on actionable steps.
    """

    response=ollama.chat(model='llama3.1:8b', messages=[{'role':'user','content':prompt}])
    print("Analysis complete!")
    return response['message']['content']

if __name__== "__main__":
    file_path = r"D:\Think Solution\gl_ic.csv"
    data_text, df = load_and_prep_data(file_path)

    print("\nInvoiceOptimizer Suggestions:")
    suggestions = analyze_with_llama(data_text)
    print(suggestions)

    #save suggestions to file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    with open(f"D:\Think Solution\suggestions_{timestamp}.txt", 'w') as f:
        f.write(suggestions)
    print("Suggestions saved to 'suggestions_{timestamp}.txt'")