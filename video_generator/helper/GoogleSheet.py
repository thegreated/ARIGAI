import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class GoogleSheet:
    def __init__(self):
        self.SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SHEET_KEY")
        self.SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        credentials = Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES
        )
        self.service = build('sheets', 'v4', credentials=credentials)
        self.sheet = self.service.spreadsheets()

    # ---------- Core Helper Methods ----------
    def get_values(self, range_str, sheet_name="PRIMARY_SHEET"):
        result = self.sheet.values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=f"{sheet_name}!{range_str}"
        ).execute()
        return result.get('values', [])

    def update_values(self, range_str, values, sheet_name="PRIMARY_SHEET"):
        body = {'values': values}
        self.sheet.values().update(
            spreadsheetId=self.SPREADSHEET_ID,
            range=f"{sheet_name}!{range_str}",
            valueInputOption="RAW",
            body=body
        ).execute()

    def clear_range(self, range_str, sheet_name="PRIMARY_SHEET"):
        self.sheet.values().clear(
            spreadsheetId=self.SPREADSHEET_ID,
            range=f"{sheet_name}!{range_str}"
        ).execute()

    def get_sheet_id(self, sheet_name):
        spreadsheet = self.sheet.get(spreadsheetId=self.SPREADSHEET_ID).execute()
        for s in spreadsheet['sheets']:
            if s['properties']['title'] == sheet_name:
                return s['properties']['sheetId']
        raise ValueError(f"Sheet '{sheet_name}' not found")

    def delete_rows(self, row_index, sheet_name="PRIMARY_SHEET"):
        sheet_id = self.get_sheet_id(sheet_name)
        request_body = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": sheet_id,
                            "dimension": "ROWS",
                            "startIndex": row_index,
                            "endIndex": row_index + 1
                        }
                    }
                }
            ]
        }
        self.sheet.batchUpdate(
            spreadsheetId=self.SPREADSHEET_ID,
            body=request_body
        ).execute()

    def insert_row(self, start_index, end_index, sheet_name="PRIMARY_SHEET"):
        sheet_id = self.get_sheet_id(sheet_name)
        request_body = {
            "requests": [
                {
                    "insertDimension": {
                        "range": {
                            "sheetId": sheet_id,
                            "dimension": "ROWS",
                            "startIndex": start_index,
                            "endIndex": end_index
                        },
                        "inheritFromBefore": False
                    }
                }
            ]
        }
        self.sheet.batchUpdate(
            spreadsheetId=self.SPREADSHEET_ID,
            body=request_body
        ).execute()

    # ---------- Business Logic ----------
    def change_status(self, title):
        currently_run = self.get_values("B13:D13")
        if currently_run:
            currently_run[0][2] = "Done"
            currently_run[0].append(title)
            self.insert_value(currently_run, "B19", "D13", 17, 18, "B18", True, delete_data="B13")

    def generate(self):
        self.check_pending()
        data = self.get_values("B7:D7")
        can_start = self.check_ongoing_data()

        if data and can_start:
            self.insert_value(data, "C7", "D7", 12, 13, "B13", delete_data="C7")
            return data[0][1]
        elif not can_start:
            print("There is an ongoing process")
            return False
        else:
            print("Currently no data available")
            return False

    def check_pending(self):
        data = self.get_values("B7:D7")
        pending_value = self.get_values("B6", "PENDING_ARTICLE")

        if pending_value and not data:
            link = pending_value[0][0]
            self.update_values("C7", [[link, "PENDING"]])
            self.clear_range("B6", "PENDING_ARTICLE")
            self.delete_rows(5, "PENDING_ARTICLE")
        else:
            print("---No pending article")

    def check_ongoing_data(self):
        return not bool(self.get_values("B13:D13"))

    def insert_value(self, values, start, end, start_idx, end_idx, update, new_tab=False, delete_data="C7"):
        self.clear_range(f"{delete_data}:{end}")

        if new_tab:
            title = values[0][3]
            row_data = [values[0][0], values[0][1], values[0][2], title]
            self.insert_row(start_idx, end_idx)
        else:
            row_data = [values[0][0], values[0][1], values[0][2]]
            self.update_values(update, [row_data])

        self.update_values(update, [row_data])

