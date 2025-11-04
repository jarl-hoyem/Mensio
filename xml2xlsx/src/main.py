"""XML to Excel.

Convert XML files to rows in an Excel file.
"""

import os
import glob
from yaml import safe_load
from modules.excel_writer import ExcelWriter


def get_xml_files(directory: str) -> list[str]:
    """Read and return the names of all XML files in a directory.

    :param: Directory, which contains the XML files.
    :return: The paths of the XML files in the directory.
    """
    return glob.glob(os.path.join(directory, "*.xml"))


def check_config_data() -> tuple[dict[str, str | dict[int, str] | list[str]], str, str]:
    """Check if the config data contains the required keys.

    :return: The config data, the XML directory and the Excel path.
    """
    # pylint: disable=too-many-try-statements
    try:
        with open("config.yaml", encoding="utf-8") as config_file:
            config = safe_load(config_file)
    except FileNotFoundError as e:
        print("ERROR: No config.yaml file found. Stopping without any action taken.")
        raise SystemExit from e
    try:
        excel: str = config["excel_path"]
        xml: str = config["xml_directory"]
    except KeyError as e:
        print("ERROR: Missing key (excel_path or xml_directory) in config.yaml. Stopping without any action taken.")
        raise SystemExit from e
    return config, xml, excel


if __name__ == "__main__":
    config_data, xml_directory, excel_path = check_config_data()
    excel_writer: ExcelWriter = ExcelWriter(config_data)
    xml_files: list[str] = get_xml_files(xml_directory)

    if excel_writer.columns_are_correct():
        if xml_files:
            for file in xml_files:
                try:
                    excel_writer.update_row(file)
                except (ValueError, KeyError, OSError) as error:
                    print(f"WARNING: Failed to process {file}: {error}. Continuing with the next file.")
        else:
            print(f"WARNING: No XML files found in the directory: {xml_directory}. Stopping without any action taken.")
    else:
        print(f"ERROR: Columns in {excel_path} are not as expected. Stopping without any action taken.")
