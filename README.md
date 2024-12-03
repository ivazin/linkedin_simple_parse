# simple linkedin parsing

A script that crawls the specified URLs of people in linkedin and writes out their full names, descriptions, last position and company.

Input `parse_input.txt`:

    https://www.linkedin.com/in/satyanadella/
    https://www.linkedin.com/in/dave-mckay-4189071/

Output `parsed_output.csv`:

    ,url,name_txt,short_about_txt,last_role,company_txt
    0,https://www.linkedin.com/in/satyanadella/,Satya Nadella,Chairman and CEO at Microsoft,Chairman and CEO,Microsoft
    1,https://www.linkedin.com/in/dave-mckay-4189071/,Dave McKay,President & CEO at RBC,President & CEO,RBC


## First run
Create virtual environment:

    python3 -m venv venv.nosync
    source venv.nosync/bin/activate
    pip install -r requirements.txt

Create `parse_input.txt` with:

    https://www.linkedin.com/in/satyanadella/
    https://www.linkedin.com/in/dave-mckay-4189071/

Run script:

    python3 parse_linkedin_data.py

Enter your login and pass to authenticate on opened LinkedIn page.
Press Enter to continue script execution.

Parsing will start.