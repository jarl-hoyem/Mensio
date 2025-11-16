"""Run the high-level tests."""

from mensio.modules.config import ConfigData, check_config_data, get_xml_files  # type: ignore[import-not-found]
from mensio.modules.excel_writer import ExcelWriter  # type: ignore[import-not-found]


def test_mensio() -> None:
    """Test mensio."""
    config_data: ConfigData = check_config_data()
    excel_writer: ExcelWriter = ExcelWriter(config_data)
    xml_files: list[str] = get_xml_files(config_data["xml_directory"])
    if excel_writer.columns_are_correct():
        if xml_files:
            for file in xml_files:
                excel_writer.update_row(file)
