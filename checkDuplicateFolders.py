import os
import re

from definitions import extractId
from definitions import MOVIES_LOCATION

if __name__ == "__main__":

    extracted_ids = []
    duplicate_ids = set()

    for folder_name in os.listdir(MOVIES_LOCATION):
        folder_id = extractId(folder_name)
        if folder_id:
            if folder_id in extracted_ids:
                duplicate_ids.add(folder_id)
            else:
                extracted_ids.append(folder_id)
        else:
            print(f"[error]: No ID in: {folder_name}")

    if duplicate_ids:
        print("\n[warning]: Duplicate IDs found!")
        print(" -- Duplicate IDs:", ", ".join(duplicate_ids))
    else: 
        print("\n[info]: No duplicate folders found!\n")
