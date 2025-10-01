import fitz  # PyMuPDF
import os
from langchain.document_loaders import PyMuPDFLoader
import pdfplumber
import io
import pandas as pd


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF with PyMuPDF and returns it as a LangChain document"""
    try:
        loader = PyMuPDFLoader(pdf_path)
        documents = loader.load()
        return documents
    except Exception as e:
        print(f"Error extracting text: {e}")
        return []


def extract_images_from_pdf(pdf_path, output_folder=os.path.join(os.path.dirname(__file__), "Data", "images")):
    """Extracts images from a PDF and saves them in a folder"""
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        pdf_document = fitz.open(pdf_path)
        image_paths = []

        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            images = page.get_images(full=True)

            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_path = os.path.join(output_folder, f"image_page_{page_num + 1}_{img_index}.{image_ext}")

                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                image_paths.append(image_path)

        pdf_document.close()
        return image_paths
    except Exception as e:
        print(f"Fehler beim Extrahieren von Bildern: {e}")
        return []


def extract_tables_from_pdf(pdf_path, output_folder=os.path.join(os.path.dirname(__file__), "Data", "tables")):
    """extracts tables from a PDF with pdfplumber and saves them as CSV files"""
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        table_paths = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                for table_idx, table in enumerate(tables, start=1):
                    df = pd.DataFrame(table[1:], columns=table[0])
                    table_path = os.path.join(output_folder, f"table_page_{page_num}_{table_idx}.csv")
                    df.to_csv(table_path, index=False, encoding="utf-8")
                    table_paths.append(table_path)

        return table_paths
    except Exception as e:
        print(f"Error extracting tables (pdfplumber): {e}")
        return []


def main(pdf_path):
    """Main function for extracting text, images and tables from a PDF"""
    # Extract text
    print("Extract text...")
    documents = extract_text_from_pdf(pdf_path)
    for doc in documents:
        print(f"Seite {doc.metadata['page'] + 1}: {doc.page_content}...")

    # Extract pictures
    print("\nExtract pictures...")
    image_paths = extract_images_from_pdf(pdf_path)
    for img_path in image_paths:
        print(f"Pictures saved: {img_path}")

    # Extract tables
    print("\nExtract tables...")
    table_paths = extract_tables_from_pdf(pdf_path)
    for table_path in table_paths:
        print(f"Table saved: {table_path}")

    # Summary of extracted content for LangChain
    extracted_content = {
        "documents": documents,
        "image_paths": image_paths,
        "table_paths": table_paths
    }

    return extracted_content


if __name__ == "__main__":
    pdf_path = os.path.join(os.path.dirname(__file__), "test4.pdf")
    try:
        extracted_content = main(pdf_path)
    except Exception as e:
        print(f"Error in the main function: {e}")
