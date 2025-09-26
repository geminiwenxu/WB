import fitz  # PyMuPDF
from pdf2image import convert_from_path
import tabula
import os
from langchain.document_loaders import PyMuPDFLoader
from langchain.schema import Document
import numpy as np
from PIL import Image
import io
import pandas as pd


def extract_text_from_pdf(pdf_path):
    """Extrahiert Text aus einem PDF mit PyMuPDF und gibt ihn als LangChain-Dokument zurück"""
    try:
        loader = PyMuPDFLoader(pdf_path)
        documents = loader.load()
        return documents
    except Exception as e:
        print(f"Fehler beim Extrahieren von Text: {e}")
        return []


def extract_images_from_pdf(pdf_path, output_folder="images"):
    """Extrahiert Bilder aus einem PDF und speichert sie in einem Ordner"""
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


def extract_tables_from_pdf(pdf_path, output_folder="tables"):
    """Extrahiert Tabellen aus einem PDF und speichert sie als CSV-Dateien"""
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Verwende tabula-py mit den funktionierenden java_options
        tables = tabula.read_pdf(
            pdf_path,
            pages="all",
            multiple_tables=True,
            # Kein GUI nötig, sicher für Serverbetrieb / Erlaubt nicht modularisiertem Code die Nutzung von nativen Funktionen
            java_options=["-Djava.awt.headless=true", "--enable-native-access=ALL-UNNAMED"]
        )
        table_paths = []

        for table_idx, table in enumerate(tables):
            table_path = os.path.join(output_folder, f"table_{table_idx + 1}.json")
            table.to_csv(table_path, index=False)
            table_paths.append(table_path)

        return table_paths
    except Exception as e:
        print(f"Fehler beim Extrahieren von Tabellen: {e}")
        return []


def main(pdf_path):
    """Hauptfunktion zum Extrahieren von Text, Bildern und Tabellen aus einem PDF"""
    # Text extrahieren
    print("Extrahiere Text...")
    documents = extract_text_from_pdf(pdf_path)
    for doc in documents:
        print(f"Seite {doc.metadata['page'] + 1}: {doc.page_content}...")

    # Bilder extrahieren
    print("\nExtrahiere Bilder...")
    image_paths = extract_images_from_pdf(pdf_path)
    for img_path in image_paths:
        print(f"Bild gespeichert: {img_path}")

    # Tabellen extrahieren
    print("\nExtrahiere Tabellen...")
    table_paths = extract_tables_from_pdf(pdf_path)
    for table_path in table_paths:
        print(f"Tabelle gespeichert: {table_path}")

    # Zusammenfassung der extrahierten Inhalte für LangChain
    extracted_content = {
        "documents": documents,
        "image_paths": image_paths,
        "table_paths": table_paths
    }

    return extracted_content


if __name__ == "__main__":
    pdf_path = r"test.pdf"
    try:
        extracted_content = main(pdf_path)
    except Exception as e:
        print(f"Fehler in der Hauptfunktion: {e}")