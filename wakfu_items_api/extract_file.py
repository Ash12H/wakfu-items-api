import json
import requests
from wakfu_items_api.version import get_current_version
from wakfu_items_api.categories import Categories
from urllib.parse import urljoin

BASE_URL = "https://wakfu.cdn.ankama.com/gamedata/"


def extract_file(category: Categories):
    version = get_current_version()
    url = urljoin(BASE_URL, f"{version}/{category}.json")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        msg = f"Error fetching version: {e}"
        raise SystemExit(msg)
    except KeyError:
        msg = "Version key not found in the response."
        raise SystemExit(msg)
    except json.JSONDecodeError:
        msg = "Error decoding JSON response."
        raise SystemExit(msg)
    except Exception as e:
        msg = f"An unexpected error occurred: {e}"
        raise SystemExit(msg)


if __name__ == "__main__":
    # Example usage
    category = Categories.items
    extracted_file = extract_file(category)
    print(f"Extracted file for category: {category}")
    print(f"Current version: {get_current_version()}")
    print(f"Extracted file (first 100 chars): \n{str(extracted_file)[:100]}")
