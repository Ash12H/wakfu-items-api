import os
from wakfu_items_api.categories import Categories
from wakfu_items_api.extract_file import extract_file
from wakfu_items_api.version import get_current_version
import json
import argparse


def extract_all_files(output_directory="."):
    """
    Extracts all files from the Wakfu API and saves them to a specified directory.
    """
    categories = [category.value for category in Categories]
    version = get_current_version()

    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_directory, exist_ok=True)

    for category in categories:
        try:
            data = extract_file(category)
            filename = os.path.join(output_directory, f"{category}_{version}.json")
            with open(filename, "w", encoding="utf-8") as extracted_file:
                json.dump(data, extracted_file, ensure_ascii=False, indent=4)
            print(f"Extracted {category} to {filename}")
        except Exception as e:
            print(f"Failed to extract {category}: {e}")
    print("All files extracted successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract all files from the Wakfu API."
    )
    parser.add_argument(
        "-o",
        "--output-directory",
        type=str,
        default=".",
        help="Directory where the extracted files will be saved. Default is the current directory.",
    )
    args = parser.parse_args()
    extract_all_files(output_directory=args.output_directory)
