"""Utilities for working with the config.yaml file."""

__all__ = ["ConfigData", "get_xml_files", "check_config_data"]

import os
import glob
from pathlib import Path
from typing import TypedDict, cast
from importlib.resources import files
from yaml import safe_load

REPO_ROOT = Path(__file__).parent.parent
CONFIG_FILE = REPO_ROOT / "config.yaml"


class ConfigData(TypedDict):
    """Type definition for the configuration YAML structure."""

    excel_path: str
    xml_directory: str
    sheet_title: str
    mapping: dict[int, str]
    excel_headings: list[str]


def get_xml_files(directory: str) -> list[str]:
    """Read and return the names of all XML files in a directory.

    :param: Directory, which contains the XML files.
    :return: The paths of the XML files in the directory.
    """
    return glob.glob(os.path.join(directory, "*.xml"))


def check_config_data() -> ConfigData:
    """Check if the config file is valid.

    Resolv all paths to absolute paths.

    :return: The prepared config data.
    """

    def _validate_path_exists(path: str) -> None:
        """Validate that a required path exists."""
        if not Path(path).exists():
            print(f"ERROR: {path} not found.")
            raise SystemExit

    try:
        config_raw = safe_load(CONFIG_FILE.read_text())
    except FileNotFoundError as e:
        print("ERROR: No config.yaml file found. Stopping without any action taken.")
        raise SystemExit from e

    # Validate all required keys exist.
    required_keys: list[str] = ["excel_path", "xml_directory", "sheet_title", "mapping", "excel_headings"]
    missing_keys: list[str] = [key for key in required_keys if key not in config_raw]
    if missing_keys:
        raise KeyError("ERROR: Missing required keys in config.yaml:", ". ".join(missing_keys))

    # Resolve paths to absolute.
    config_dir = Path(str(files("mensio"))).resolve()
    config: ConfigData = {
        "excel_path": str((config_dir / config_raw["excel_path"]).resolve()),
        "xml_directory": str((config_dir / config_raw["xml_directory"]).resolve()),
        "sheet_title": str(config_raw["sheet_title"]),
        "mapping": cast(dict[int, str], config_raw["mapping"]),
        "excel_headings": list(config_raw["excel_headings"]),
    }

    _validate_path_exists(config["excel_path"])
    _validate_path_exists(config["xml_directory"])

    return config
