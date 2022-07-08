from dotenv import load_dotenv
from pprint import pprint
from sheet import Sheet
from pprint import pprint

import os

load_dotenv()

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
FILENAME = os.environ.get("FILENAME")
SPREADSHEET_NAME = os.environ.get("SPREADSHEET_NAME")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def main():

    ranges = [
        f"'{SPREADSHEET_NAME}'!{x}" for x in ["A:A", "D:D", "G:G", "H:H"]
    ]
    sheet = Sheet(FILENAME, SCOPES, SPREADSHEET_NAME)
    result = sheet.values_batch_get(spreadsheet_id=SPREADSHEET_ID,
                                    ranges=ranges)

    pprint(result)


if __name__ == "__main__":
    main()
