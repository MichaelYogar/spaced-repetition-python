import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from google.oauth2 import service_account
from pprint import pprint

load_dotenv()

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
FILENAME = os.environ.get("FILENAME")
SPREADSHEET_NAME = os.environ.get("SPREADSHEET_NAME")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def main():

    credentials = service_account.Credentials.from_service_account_file(
        FILENAME, scopes=SCOPES)
    service = build("sheets", "v4", credentials=credentials)

    request = service.spreadsheets().values().batchGet(
        spreadsheetId=SPREADSHEET_ID,
        ranges=[f"'{SPREADSHEET_NAME}'!{x}" for x in ["A:A", "G:G"]])
    response = request.execute()
    pprint(response["valueRanges"])


if __name__ == "__main__":
    main()
