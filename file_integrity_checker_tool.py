import hashlib
import os
import json

# Path to store known file hashes
HASH_RECORD_FILE = 'file_hashes.json'

# Function to calculate SHA-256 hash of a file
def calculate_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        print(f" File not found: {filepath}")
        return None

# Load previously stored hashes
def load_known_hashes():
    if os.path.exists(HASH_RECORD_FILE):
        with open(HASH_RECORD_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save current hashes to file
def save_hashes(hashes):
    with open(HASH_RECORD_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

# Main function to check integrity
def check_integrity(directory):
    known_hashes = load_known_hashes()
    current_hashes = {}
    changed_files = []
    new_files = []

    print(f"🔍 Scanning directory: {directory}\n")

    for root, _, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            file_hash = calculate_hash(filepath)
            if not file_hash:
                continue
            relative_path = os.path.relpath(filepath, directory)
            current_hashes[relative_path] = file_hash

            if relative_path in known_hashes:
                if known_hashes[relative_path] != file_hash:
                    changed_files.append(relative_path)
            else:
                new_files.append(relative_path)

    # Save updated hashes
    save_hashes(current_hashes)

    # Report
    if not changed_files and not new_files:
        print(" All files are intact. No changes detected.")
    else:
        if changed_files:
            print(" Changed files:")
            for f in changed_files:
                print(f" - {f}")
        if new_files:
            print("\n New files added:")
            for f in new_files:
                print(f" - {f}")

# ---------- Run Script ----------
if __name__ == "__main__":
    directory_to_check = input(" Enter directory path to check: ").strip()
    if os.path.isdir(directory_to_check):
        check_integrity(directory_to_check)
    else:
        print(" Invalid directory. Please try again.")
