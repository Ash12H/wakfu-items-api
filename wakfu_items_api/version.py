import json
import requests


VERSION_ADRESS = "https://wakfu.cdn.ankama.com/gamedata/config.json"


def get_current_version() -> str:
    """
    Fetches the current version of the game from the specified URL.

    Returns:
        str: The current version of the game.
    """
    try:
        response = requests.get(VERSION_ADRESS)
        response.raise_for_status()
        data = response.json()
        return data["version"]
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
    current_version = get_current_version()
    print(f"Current version: {current_version}")
