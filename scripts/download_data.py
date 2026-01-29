"""
Script Name:  download_data.py
Description:  A utility to download sample medical PDF data for the RAG Chatbot.
Author:       Michael R. Rutherford
Date:         2026-01-28

Copyright (c) 2026
License: MIT
"""

import os
import requests

# Configuration
from app.core.config import DATA_DIR
PDF_SOURCES: list[dict[str, str]] = [
    {
        "url": "https://www.cms.gov/Medicare/Provider-Enrollment-and-Certification/CertificationandComplianc/Downloads/Emergency-Prep-Rule.pdf", 
        "name": "cms_emergency_prep.pdf" 
    }
]

def ensure_directory_exists(directory: str) -> None:
    """Creates the data directory if it does not exist."""
    os.makedirs(directory, exist_ok=True)

def download_file(url: str, filename: str) -> None:
    """
    Downloads a file from a specified URL to the data directory.
    
    Args:
        url (str): The source URL of the file.
        filename (str): The destination filename.
    """
    local_path = os.path.join(DATA_DIR, filename)
    
    # Avoid re-downloading existing files to save bandwidth and time
    if os.path.exists(local_path):
        print(f"Skipping: {filename} (Already exists)")
        return

    print(f"Downloading: {filename}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
            
        print(f"Success: {filename}")
        
    except requests.RequestException as e:
        print(f"Error downloading {filename}: {e}")

if __name__ == "__main__":
    ensure_directory_exists(DATA_DIR)
    
    for item in PDF_SOURCES:
        download_file(item["url"], item["name"])
