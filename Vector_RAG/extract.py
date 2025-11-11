import email
from email import policy
from email.parser import BytesParser
#imports for table:
import camelot
import pandas as pd
from typing import List
import tempfile
import shutil
import atexit
import os


def extract_mail_for_rag(file):
    """ Extract information from a Mail file """
    with open(file, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    subject = msg["Subject"]
    sender = msg["From"]

    if msg.is_multipart():
        body = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_content()
    else:
        body = msg.get_content()

    document = f"From: {sender}\nSubject: {subject}\n{body}"

    return document

import pandas as pd

def extract_excel_for_rag(file):
    """ Extract information from an Excel file """
    df = pd.read_excel(file)

    documents=[]
    for i, row in df.iterrows():
        text = " | ".join(f"{col}: {row[col]}" for col in df.columns)
        documents.append(text)

    return documents

#------- Table -------
def extract_tables(pdf_file: str, flavor: str = 'lattice') -> List[pd.DataFrame]:
    """
    Extrahiert Tabellen aus PDF mit Camelot.
    - 'lattice': Tabellen mit Linien (benutzt Poppler)
    - 'stream' : Tabellen mit Leerzeichen (keine Temp-Dateien)
    """
    print(f"Extraction from '{pdf_file}' with Flavor: '{flavor}'...")

    # --- Joint Parameter ---
    common_kwargs = {
        "filepath": pdf_file,
        "pages": 'all',
        "strip_text": '\n',
        "flag_size": True,
    }

    # --- Flavor-spezifische Parameter ---
    if flavor == 'lattice':
        # Only lattice-specific Parameter
        kwargs = {
            **common_kwargs,
            "flavor": "lattice",
        }
    elif flavor == 'stream':
        # Temp-Verzeichnis only allowed by stream
        temp_dir = tempfile.mkdtemp(prefix="camelot_stream_")

        def cleanup():
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass
        atexit.register(cleanup)

        kwargs = {
            **common_kwargs,
            "flavor": "stream",
            "edge_tol": 50,
            "row_tol": 15,
            "temp_dir": temp_dir,
        }
    else:
        raise ValueError("flavor must be 'lattice' or 'stream'")

    try:
        tables = camelot.read_pdf(**kwargs)

        dfs = []
        for i, table in enumerate(tables):
            df = table.df
            # Clean up: remove empty rows/columns
            df = df.replace(r'^\s*$', pd.NA, regex=True)
            df = df.dropna(how='all').dropna(axis=1, how='all')
            dfs.append(df)
            print(f"  Table {i+1}: {df.shape[0]} rows x {df.shape[1]} cols")

        print(f"Extraktion finished. {len(dfs)} Table(s) found.")
        return dfs

    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        # Cleanup nur bei stream
        if flavor == 'stream' and 'temp_dir' in locals():
            cleanup()
            atexit.unregister(cleanup)

def extract_tables_for_rag(pdf_file: str, flavor: str = 'lattice') -> List[str]:
    """
    Extract tables from PDFs -> RAG-friendly Strings: "column: value | column: value"
    """
    dfs = extract_tables(pdf_file, flavor=flavor)
    rag_documents = []

    for idx, df in enumerate(dfs):
        if df.empty:
            continue

        # Clean up column names
        df.columns = [str(col).strip() for col in df.columns]

        # Count valid numers for Log
        valid_row_count = 0

        for _, row in df.iterrows():  # _ ist (index, Series)
            row_items = []
            for col in df.columns:
                cell_value = str(row[col]).strip()
                if cell_value and cell_value.lower() not in ['nan', 'none', '']:
                    row_items.append(f"{col}: {cell_value}")

            if row_items:
                text = " | ".join(row_items)
                rag_documents.append(text)
                valid_row_count += 1

        print(f"  -> Table {idx+1}: {len(df)} Column -> {valid_row_count} RAG-Dokument")

    print(f"Total: {len(rag_documents)} RAG-Dokuments created from tables.")
    return rag_documents
