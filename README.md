1. Save the folder src on your computer.

2. Install Python from:
   https://www.python.org/downloads/

3. Save the file pip.ini in the path %APPDATA%\pip\.

4. In a terminal change your current directory to src:
   cd C:\<my top directory>\<my subdirectory>\ ... \src.

5. run python -m pip install -r requirements.txt

6. Check the data in the file config.yaml is correct and set the paths if needed.

7. run: python .\main.py

8. Note that the library used, openpyxl, does not support external links, macros and pivot tables in Excel.
If these are present in your Excel file, running the program will corrupt the Excel file!