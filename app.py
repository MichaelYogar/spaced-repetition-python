from dotenv import load_dotenv
from pprint import pprint

from sheet import Sheet
from pprint import pprint
from pandas_utils import drop_rows_by_filter
from datetime import datetime as DateTime, timedelta as TimeDelta

import sys
import pandas as pd
import os

load_dotenv()

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
FILENAME = os.environ.get("FILENAME")
SPREADSHEET_NAME = os.environ.get("SPREADSHEET_NAME")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def calculate_due_date(date, repeat):
    match repeat:
        case "1":
            return date + TimeDelta(days=1)
        case "2":
            return date + TimeDelta(days=3)
        case "3":
            return date + TimeDelta(days=7)
        case _:
            return date

def get_required_rows(df):
    """
    :param Dateframe with `Needs Review` == 1 \n
    Needs Review and Repeated:
                1 times -> Due 1 day from entry date. \n
                2 times -> Due 3 day from entry date. \n
                3 times -> Due 7 day from entry date \n
    """

    # Get only rows that need review
    drop_rows_by_filter(df, filter = df['Needs Review'] == "0")

    # Pandas dateframe to 2-D List
    result = [[x, y, z] for x, y, z in zip(df['Date'], df['Problem'], df['Repeat'])]

    # Required questions based on Spatial Repetition
    today = DateTime.now()
    for date_entry, problem, repeats in result:
        datetime_object = DateTime.strptime(date_entry, '%d-%b')
        date = calculate_due_date(datetime_object, repeats)
        if date.day == today.day and date.month == today.month:
            # Output questions to do
            print(problem)

def flatten_list(list2d):
    new_list = []
    for data in list2d:
        # Keep entries with empty cells
        new_list.append(data[0] if data else None) 
    return new_list

def get_longest_subarray(list2D):
    return max(list2D, key=len)

def sheet_data_to_df(sheet_data):
    if Sheet.is_valid_sheet_data(sheet_data):
        # Convert into list[ValueRange] into dict[header, values]
        dict = {}
        for col in sheet_data:
            flat_list = flatten_list(col['values'][1:])
            dict[col['values'][0][0]] = flat_list

        values = dict.values()
        maxLen = len(get_longest_subarray(values))

        for value in values:
            if len(value) < maxLen:
                # Ensure each column is the same length
                value.extend([None]*(maxLen - len(value)))

        df = pd.DataFrame(dict, columns=dict.keys())

        # Remove rows with empty cells
        df.dropna(inplace=True)
        return df
    else:
        raise ValueError("Invalid Sheet data")

def main():
    try:
        ranges = [
            f"'{SPREADSHEET_NAME}'!{x}" for x in ["A:A", "C:C", "G:G", "H:H"]
        ]
        sheet = Sheet(FILENAME, SCOPES, SPREADSHEET_NAME)
        data = sheet.values_batch_get(spreadsheet_id=SPREADSHEET_ID,
                                        ranges=ranges)
        df = sheet_data_to_df(data)
        get_required_rows(df)

    except ValueError as exp:
        print ("Error:", exp)
        sys.exit()

if __name__ == "__main__":
    main()
