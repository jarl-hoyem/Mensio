# Software Requirements Specification

## Introduction

Background:For a medical thesis measurements are captured with a software tool.
The measurements are stored in XML files. From these we want to extract the most important data.
Then we want to copy it to an Excel spreadsheet named 2025-09_24_Patient_Measurements_VX.xlsx
So far this was done by hand. An automated tool would save time in collecting the data.

The requirements received via email and orally are summarized below.

The XML files are stored in the folder "Datenaus3Mensio". There are thousands of XML files.
The files are named according to the patient names "Surname, Firstname.xml". However, these
filenames cannot be used as comparison for the data as often errors occur due to German umlauts.

Hence, the patient ID has to be found in the Excel sheet "tavi_mock_1000_with_G". Then the
measurements can be assigned to the right patient. If a patient ID is not found in the
Excel sheet, a warning is displayed, and the patient is ignored.

The sheet "tavi_mock_1000_with_G" has to be identified by its name. There are other sheets
with different names in the Excel file. Now the data from the XML files has to be copied
to the right cell in the row with the same patient ID.

The tags in the XML files are mapped to the headings in the Excel sheet. Data in the Excel
sheet must NEVER be overwritten!

The Excel columns A-F should NEVER be overwritten! They are there for reference.

The program has to run under Windows.

In the test data note the following:

Patient number 5: An example where the Agatston Score was not written in the XML file.
Hence, it was added manually to the Excel sheet. Do not overwrite the Agatston Score!

Patient number 9: An example where the Agatston Score was not recorded at all. Hence,
"NA" was added manually. Do not overwrite this either. Also, the RRInterval was not
recorded at all and hence "NA" was added manually. Do not overwrite this either.
Possibly the XML file contains suspicious data, which we do not want.

PatientID should be used to find the right patient in the Excel sheet.
PatientName and PatientBirthDate should already be in the Excel sheet. Only use this
when the patient is not found.

### Purpose

The goal of the project is to save time in recording measurements to an Excel file
for further analysis. Further an objective is to avoid human errors when transferring
the data by hand.

### Intended audience

Developer and users.

### Scope

The project should be completed in time to be useful for the medical thesis. This handing
in of the thesis has a hard deadline.

## General description

A real world need to transform data from one format to another. Previously this was done by
hand. Doable in the given time. Main challenge:Understand the user needs.

### Product Features

Reads XML files and writes data in the appropiate lines in an Excel file.

### User class and characteristics

The users are medical students completing their thesis.

### Operating environment

A computer at a hospital. Operating system:Windows.

### Constraints

For data privacy reasons the developer has no access to the computer nor to the
actual files needed to be manipulated.

### Assumptions and dependencies

* Python can be installed on the computer.
* Run time is not an issue.

## System requirements

Must run Python.

### Functional requirements

The mapping of XML tags to the Excel columns headings was extracted and stored
in a separate file for reference. File name: "XML_to_Excel_mapping.txt".

1. Never overwrite pre-filled Excel cells.
2. XML file has patient ID not in Excel -> Error message.
The original requirement was to write these in a separate sheet. However, these were so few
and had to be checked anyway. Hence, it was agreed such cases would be done by hand as
previously.
3. Check headings are as expected in Excel before writing:Avoids wrong writes if a column
was added (or removed) by mistake.
4. Plausibility check on value RRInterval.
5. Swap point '.' for comma ',' before writing. XML uses point as fraction delimiter as
standard in English. The Excel uses comma as fraction delimiter as this is the German
number format.
6. Round all numbers to 1 decimal place except:
7. The following which should be rounded to 0 decimals -> integers:

   * RRinterval
   * Calcium
   * Agatston

8. Comment the code on how to change the decimal places.
9. Mark the values yellow to indicate an automatically written value.

    #### Derived requirements

10. Use yaml file for mapping and specifying directories.
11. Format values as number instead of text coming from XML.
12. Add a note in the README.md about external links and pivot tables not allowed by openpyxl.

    #### Rejected Requirements
13. Check that there are no double patient IDs.
That is, no two rows where the column "Intellispace (KARD_PATIENT.IDENTNA)"
has identical values.

This can be easily done with Excel, so there is no need to use Python for it.

## External interface requirements

XML and Excel.

### User Interfaces

The user should:

* Install Python
* Edit the yaml file
* Run the program

### Software Interfaces

XML and Excel.

## Non-Functional Requirements

None.

### Performance requirements

None.

### Safety requirements

None.

### Security requirements

Patient data must stay private at all time.

### Software quality attributes

Should be usable and extendable in the future. For example for a new medical student
with some Python knowledge. Hence, it should be of a reasonable quality and well
documented.