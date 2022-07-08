from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


class Sheet:
    """A wrapper class for Google Sheets API v4.

    Usage Limits: 300 per minute for Read/Write requests.
    Built in rate limiter that delays API calls if exceeds usage.
    """

    def __init__(self, filename, scopes, sheet_name):
        """
        :param filename The path to the service account json file
        :param scopes
        :param sheet_name
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename,
            scopes=scopes,
        )
        self.service = build("sheets", "v4", credentials=credentials)
        self.sheet_name = sheet_name

    def values_batch_get(self, spreadsheet_id, ranges, major_dimension="ROWS"):
        """Returns one or more ranges of values from a spreadsheet.
        :param spreadsheet_id:  The ID of the spreadsheet to retrieve data from.
        :param value_ranges:    The A1 notation of the range to retrieve values from.
        :param major_dimension: The major dimension that results should use.
        :return: `ValueRange`

        """
        request = self.service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id,
            ranges=ranges,
            majorDimension=major_dimension,
        )
        response = self._make_request(request)
        return response.get('valueRanges', [])

    # TODO: add rate limiting
    def _make_request(self, request):
        response = request.execute()
        return response
