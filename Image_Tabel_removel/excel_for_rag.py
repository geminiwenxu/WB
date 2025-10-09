import pandas as pd

def extract_excel_for_rag(file):
    """ Extract information from an Excel file """
    df = pd.read_excel(file)

    documents=[]
    for i, row in df.iterrows():
        text = " | ".join(f"{col}: {row[col]}" for col in df.columns)
        documents.append(text)

    return documents