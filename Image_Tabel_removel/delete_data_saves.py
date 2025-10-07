import os

def delete_data():
    # Ordnerpfade
    folders = ["Data/images", "Data/tables"]

    for folder in folders:
        if os.path.exists(folder):
            for file_name in os.listdir(folder):
                file_path = os.path.join(folder, file_name)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        import shutil
                        shutil.rmtree(file_path)
                    print(f"Gelöscht: {file_path}")
                except Exception as e:
                    print(f"Fehler beim Löschen von {file_path}: {e}")
        else:
            print(f"Ordner nicht gefunden: {folder}")

delete_data()