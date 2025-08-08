
#1hzb2HzrW5MYh9C7TybMiO9cseU-vVBjWejylU9elcrQ/edit?gid=0#gid=0

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import  os
from dotenv import load_dotenv
class GoogleSheet:



    def __init__(self):

        self.SERVICE_ACCOUNT_FILE =os.getenv("GOOGLE_SHEET_KEY")
        self.SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.service = build('sheets', 'v4', credentials=credentials)
        self.sheet = self.service.spreadsheets()

    def change_status(self,title):
        currently_run = self.check_data("B13", "D13")
        currently_run[0][2] = "Done"
        currently_run[0].append(title)

        if currently_run:
            self.insert_value(currently_run, "B19", "D13", 17, 18, "B18", True,delete_data = "B13")



    def generate(self):

        data = self.check_data("B7","D7")
        data_b13 = self.check_ongoing_data()


        if data and data_b13:
            self.insert_value(data,"C7","D7",12,13,"B13",delete_data = "C7")
            return data[0][1]
        if not data_b13:
            print("There are on going process")
            return False
        else:
            print("Currently no data on it:")
            return False






    def check_data(self,start,end):
        range = start+':'+end
        sheet_read = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=range).execute()

        values = sheet_read.get('values', [])

        if values:
            return  values
        else:
            return []

    def check_ongoing_data(self):
        range = 'B13:D13'
        sheet_read = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=range).execute()

        values = sheet_read.get('values', [])

        if values:
            return False
        else:
            return True

    def insert_value(self,values,start,end,start_,end_,update,new_tab=False,delete_data = "C7"):
        id = values[0][0]
        link = values[0][1]
        status = values[0][2]
        value = ""
        # now got data delete the row
        self.sheet.values().clear(
            spreadsheetId=self.SPREADSHEET_ID,
            range="PRIMARY_SHEET!" + delete_data + ":" + end
        ).execute()

        if new_tab:
            title = values[0][3]
            value = [id, link, status,title]
            self.insert_row(start_,end_)
        else:
            value = [id, link, status]
            self.insert(update,values)
        # Insert the data needed
        data = {
            'values': [value]
        }

        self.sheet.values().update(
            spreadsheetId=self.SPREADSHEET_ID,
            range="PRIMARY_SHEET!"+update,
            valueInputOption="RAW",
            body=data
        ).execute()

    def insert_row(self,start,end):
        insert_request = {
            "insertDimension": {
                "range": {
                    "sheetId": 0,           # 0 = first sheet; update if needed
                    "dimension": "ROWS",
                    "startIndex": start,       # 0-based index; 12 = before row 13
                    "endIndex": end
                },
                "inheritFromBefore": False
            }
        }

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.SPREADSHEET_ID,
            body={"requests": [insert_request]}
        ).execute()


    def insert(self,start,values):
        id = values[0][0]
        link = values[0][1]
        status = values[0][2]
        data = {
            'values': [[id, link, status]]
        }
        self.sheet.values().update(
            spreadsheetId=self.SPREADSHEET_ID,
            range="PRIMARY_SHEET!"+start,
            valueInputOption="RAW",
            body=data
        ).execute()


    def delete_row(self,start,end):
        self.sheet.values().clear(
            spreadsheetId=self.SPREADSHEET_ID,
            range="PRIMARY_SHEET!"+start+":"+end
        ).execute()



