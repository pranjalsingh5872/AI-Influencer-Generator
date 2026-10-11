"""
Download and Extract Blender Studio Official Human Base Meshes (CC0)
=====================================================================
Direct from Blender Foundation:
https://download.blender.org/demo/asset-bundles/human-base-meshes/
"""

import os
import sys
import urllib.request
import zipfile

URL = "https://download.blender.org/demo/asset-bundles/human-base-meshes/human-base-meshes-bundle-v1.4.1.zip"
ZIP_PATH = "human_base_meshes.zip"
EXTRACT_DIR = "blender_assets/human_base_meshes"

def download_and_extract():
    os.makedirs("blender_assets", exist_ok=True)
    
    if not os.path.exists(ZIP_PATH):
        print(f"[*] Downloading Blender Studio Human Base Meshes (v1.4.1, ~50MB)...")
        print(f"[*] Source: {URL}")
        
        def progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                if block_num % 100 == 0:
                    print(f"    Progress: {percent:.1f}% ({downloaded / 1024 / 1024:.1f} MB / {total_size / 1024 / 1024:.1f} MB)")

        urllib.request.urlretrieve(URL, ZIP_PATH, reporthook=progress)
        print(f"[+] Download complete: {ZIP_PATH}")
    else:
        print(f"[*] Using existing zip: {ZIP_PATH}")

    print(f"[*] Extracting to '{EXTRACT_DIR}'...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)
    
    print(f"[SUCCESS] Extracted assets into: {EXTRACT_DIR}")
    
    # List files extracted
    extracted_files = []
    for root, dirs, files in os.walk(EXTRACT_DIR):
        for f in files:
            if f.endswith(('.blend', '.fbx', '.obj')):
                extracted_files.append(os.path.join(root, f))
                
    print("[*] Available Blender assets:")
    for ef in extracted_files:
        print(f"    - {ef}")

if __name__ == "__main__":
    download_and_extract()
