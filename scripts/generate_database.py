import json
from wakfu_items_api.categories import Categories
from wakfu_items_api.database.actions import create_action_from_dict
from wakfu_items_api.database.item_types import create_item_type_from_dict
from wakfu_items_api.database.item_properties import create_item_property_from_dict
from wakfu_items_api.database.states import create_state_from_dict
from wakfu_items_api.database.items import create_item_from_dict
from wakfu_items_api.extract_file import extract_file
from wakfu_items_api.version import get_current_version
from pathlib import Path
import argparse
from sqlmodel import SQLModel, Session, create_engine
from tqdm import tqdm

ITEMS_CATEGORIES = {
    Categories.actions: create_action_from_dict,
    Categories.itemTypes: create_item_type_from_dict,
    Categories.equipmentItemTypes: create_item_type_from_dict,
    Categories.itemProperties: create_item_property_from_dict,
    Categories.states: create_state_from_dict,
    Categories.items: create_item_from_dict,
}
"""Order of categories to be extracted. Used to generate tables in the database."""


def add_to_db(item, engine, verbose=True) -> None:
    """Adds an item to the database. If the item already exists, it skips it."""
    with Session(engine) as session:
        try:
            session.add(item)
            session.commit()
        except Exception as e:
            session.rollback()
            if "UNIQUE constraint failed" in str(e.orig):
                if verbose:
                    print(f"Duplicate entry for {item}, skipping.")
            else:
                raise e


def generate_database(
    version: str,
    output_path: str,
    database_url: str,
    input_path: str = None,
    verbose: bool = True,
) -> None:
    """
    Extracts all files from the Wakfu API and saves them to a specified directory.
    """

    def generate_filepath(category: str) -> str:
        """
        Generates the file path for the extracted file based on the category and version.
        """
        return Path(output_path) / f"{category}_{version}.json"

    DATABASE_URL = f"{database_url}{Path(output_path) / 'database.db'}"
    engine = create_engine(DATABASE_URL, echo=False)
    SQLModel.metadata.create_all(engine)

    for category, generate_function in ITEMS_CATEGORIES.items():
        if input_path is None:
            data = extract_file(category)
        else:
            with (Path(input_path) / generate_filepath(category)).open("r") as file:
                data = json.load(file)
        for element in tqdm(data, desc=f"Processing {category}"):
            add_to_db(generate_function(element), engine, verbose=verbose)


def main() -> None:
    """
    Main function to run the script.
    """
    parser = argparse.ArgumentParser(
        description="Extract all files from the Wakfu API."
    )
    parser.add_argument(
        "-i",
        "--indir",
        type=str,
        default=None,
        help=(
            "If JSON files are already extracted, specify the directory where they are located. "
            "By default, the script will extract them directly from the Wakfu API."
        ),
    )
    parser.add_argument(
        "-o",
        "--outdir",
        type=str,
        default=".",
        help="Directory where the generated database will be saved. Default is the current directory.",
    )
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default=get_current_version(),
        help="Version of the files to be extracted. Default is the current version.",
    )
    parser.add_argument(
        "-d",
        "--database",
        type=str,
        default="sqlite:///",
        help="Database URL. Default is `sqlite:///`",
    )
    parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        default=False,
        help="Show duplicate entry warnings (default: False)",
    )
    args = parser.parse_args()
    generate_database(
        version=args.version,
        output_path=args.outdir,
        database_url=args.database,
        input_path=args.indir,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
