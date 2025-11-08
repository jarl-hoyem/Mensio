"""Utilities for working with config.yaml file."""

import os
import glob
from pathlib import Path
from typing import TypedDict, cast
from yaml import safe_load
from importlib.resources import files


class ConfigData(TypedDict):
    """Type definition for config.yaml structure."""

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
    config_file = files("src").joinpath("config.yaml")
    try:
        config_raw = safe_load(config_file.read_text())
    except FileNotFoundError as e:
        print("ERROR: No config.yaml file found. Stopping without any action taken.")
        raise SystemExit from e

    # Validate all required keys exist.
    required_keys: list[str] = ["excel_path", "xml_directory", "sheet_title", "mapping", "excel_headings"]
    missing_keys: list[str] = [key for key in required_keys if key not in config_raw]
    if missing_keys:
        raise KeyError(f"ERROR: Missing required keys in config.yaml: {'. '.join(missing_keys)}")

    # Resolve paths to absolute.
    config_dir = Path(str(files("src"))).resolve()
    config: ConfigData = {
        "excel_path": str((config_dir / config_raw["excel_path"]).resolve()),
        "xml_directory": str((config_dir / config_raw["xml_directory"]).resolve()),
        "sheet_title": str(config_raw["sheet_title"]),
        "mapping": cast(dict[int, str], config_raw["mapping"]),
        "excel_headings": list(config_raw["excel_headings"]),
    }

    # Validate files exist.
    try:
        if not Path(config["excel_path"]).exists():
            raise FileNotFoundError(f"ERROR: Excel file not found at {config['excel_path']}")
        if not Path(config["xml_directory"]).exists():
            raise FileNotFoundError(f"ERROR: Excel directory not found at {config['xml_directory']}")
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        raise SystemExit from e

    return config
