import argparse
import os
from wakfu_items_api.parser_schema import generate_uml, ItemFileSchema


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a UML diagram for the Wakfu Items API."
    )
    parser.add_argument(
        "-o",
        "--output-directory",
        type=str,
        default=".",
        help="Directory where the UML diagram will be saved. Default is the current directory.",
    )
    args = parser.parse_args()

    output_path = os.path.join(args.output_directory, "items_uml")
    generate_uml(ItemFileSchema, output_file=output_path)
