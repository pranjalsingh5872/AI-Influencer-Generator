import os
import zipfile

ZIP_PATH = "blender_assets/human_base_meshes.zip"
EXTRACT_DIR = "blender_assets/human_base_meshes"

def extract():
    if not os.path.exists(ZIP_PATH):
        print(f"[!] Zip not found at {ZIP_PATH}")
        return
    print(f"[*] Extracting {ZIP_PATH} to {EXTRACT_DIR}...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)
    print(f"[SUCCESS] Extracted assets into: {EXTRACT_DIR}")

if __name__ == "__main__":
    extract()
