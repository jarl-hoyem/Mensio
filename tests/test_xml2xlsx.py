"""High level tests."""

from main import check_config_data, get_xml_files
from modules.excel_writer import ExcelWriter


def test_xml2xlsx():
    """Test src."""
    config_data, xml_directory, excel_path = check_config_data()
    excel_writer: ExcelWriter = ExcelWriter(config_data)
    xml_files: list[str] = get_xml_files(xml_directory)
