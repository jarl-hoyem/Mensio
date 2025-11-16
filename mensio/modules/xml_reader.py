"""XML reader."""

from typing import cast
from bs4 import BeautifulSoup
from bs4.element import Tag, AttributeValueList, ResultSet


class XMLReader:
    """Read and extract specific tag values from an XML file.

    Parse an XML file and retrieve values of specific
    tags.

    Methods:
        __init__:The constructor initializes a list of tags and calls _read_file.
        _read_file: Reads the XML file and parses it with BeautifulSoup.
        get_values: Returns the read values from the XML file as a dictionary {tag: value}.
    """

    def __init__(self, file_path: str, tags: list[str]) -> None:
        """Construct the object with the filename and tags to extract.

        :param  file_path: The name of the XML file to process.
                tags: List of tags to extract values from.
        :ivar:  _file_path: Path of the XML file.
                _soup: Parsed XML file as an object to extract the values from.
                _tags: List of tags to get values for.
        Calls: _read_file()
        """
        self._file_path: str = file_path
        self._soup: BeautifulSoup = BeautifulSoup("xml", features="lxml")
        self._tags: list[str] = tags
        self._read_file()

    def _read_file(self) -> None:
        """Read and parse the data inside the XML file with BeautifulSoup."""
        try:
            with open(self._file_path, encoding="utf-8") as f:
                xml_data: str = f.read()
        except FileNotFoundError as e:
            print(f"ERROR: File {self._file_path} not found.")
            raise SystemExit from e

        self._soup = BeautifulSoup(xml_data, "xml")

    def get_path(self) -> str:
        """Get the path of the XML file."""
        return self._file_path

    def get_values(self) -> dict[str, str]:
        """Get the XML values from the file.

        :return: Tags and values from the file. If we cannot find the tag, return the value 'missing'.
        """
        return_value: dict[str, str] = {}
        # Set all values to 'missing'. Overwrite with XML values later if found.
        for tag in self._tags:
            return_value[tag] = "missing"

        # Get Non-Measurement values, here 3.
        non_measurements: list[str] = self._tags[:3]
        for tag in non_measurements:
            found_tag = self._soup.find(tag)
            if found_tag is not None and found_tag.text:
                return_value[tag] = found_tag.text
            # else: keep the default value: 'missing'.

        # Find all wanted measurement tags.
        wanted_measurements: list[str] = [m for m in self._tags if m not in non_measurements]
        # PyCharm needs the cast, mypy does not.
        measurements: ResultSet[Tag] = cast(  # type: ignore[redundant-cast]
            ResultSet[Tag], self._soup.find_all("Measurement")
        )

        # Collect wanted measurement IDs and their values.
        for measurement in measurements:
            measurement_id: str | AttributeValueList | None = measurement.get("Id")
            if measurement_id is not None and measurement_id in wanted_measurements:
                # PyCharm needs the cast, mypy does not.
                reportable_value: Tag | None = \
                    cast(Tag | None, measurement.find("ReportableValue"))  # type: ignore[redundant-cast]
                if reportable_value:
                    value: str | AttributeValueList | None = reportable_value.get("Value")
                    if value is not None:
                        return_value[cast(str, measurement_id)] = cast(str, reportable_value.get("Value"))
        return return_value
