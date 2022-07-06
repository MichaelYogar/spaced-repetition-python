import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from google.oauth2 import service_account
from pprint import pprint

load_dotenv()

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
FILENAME = os.environ.get("FILENAME")


def main():

    credentials = service_account.Credentials.from_service_account_file(
        FILENAME, scopes=SCOPES)
    service = build("sheets", "v4", credentials=credentials)

    request = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="A1:D61",
    )
    response = request.execute()
    pprint(response)


if __name__ == "__main__":
    main()
