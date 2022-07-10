from dotenv import load_dotenv
from pprint import pprint
from sheet import Sheet
from pprint import pprint

import pandas as pd
import os

load_dotenv()

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
FILENAME = os.environ.get("FILENAME")
SPREADSHEET_NAME = os.environ.get("SPREADSHEET_NAME")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def flatten_list(list2d):
    new_list = []
    for data in list2d:
        # Keep entries with empty cells
        new_list.append(data[0] if data else None) 
    return new_list

def sheet_data_to_df(sheet_data):
    # Convert into list[ValueRange] into dict[header, values]
    dict = {}
    for col in sheet_data:
        flat_list = flatten_list(col['values'][1:])
        dict[col['values'][0][0]] = flat_list


    maxLen = len(max(dict.values()))
    for value in dict.values():
        if len(value) < maxLen:
            # Ensure each column is the same length
            value.extend([None]*(maxLen - len(value)))

    df = pd.DataFrame(dict, columns=dict.keys())
    return df


def main():

    ranges = [
        f"'{SPREADSHEET_NAME}'!{x}" for x in ["A:A", "C:C", "G:G", "H:H"]
    ]
    sheet = Sheet(FILENAME, SCOPES, SPREADSHEET_NAME)
    data = sheet.values_batch_get(spreadsheet_id=SPREADSHEET_ID,
                                    ranges=ranges)

    df = sheet_data_to_df(data)

    # Remove rows with empty cells
    df.dropna(inplace=True)


if __name__ == "__main__":
    main()
