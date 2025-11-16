"""XML to Excel.

Convert XML files to rows in an Excel file.
"""

from .modules.config import ConfigData, get_xml_files, check_config_data
from .modules.excel_writer import ExcelWriter

if __name__ == "__main__":
    config_data: ConfigData = check_config_data()
    excel_writer: ExcelWriter = ExcelWriter(config_data)
    xml_files: list[str] = get_xml_files(config_data["xml_directory"])

    if excel_writer.columns_are_correct():
        if xml_files:
            for file in xml_files:
                try:
                    excel_writer.update_row(file)
                except (ValueError, KeyError, OSError) as error:
                    print(f"WARNING: Failed to process {file}: {error}. Continuing with the next file.")
        else:
            print("WARNING: No XML files found in the directory:", config_data["xml_directory"])
            print("Stopping without any action taken.")
    else:
        print(f'ERROR: Columns in {config_data["excel_path"]} are not as expected. Stopping without any action taken.')
