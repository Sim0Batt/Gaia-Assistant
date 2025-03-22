from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pickle
from datetime import datetime
import pdfplumber

class PDFDriveManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.today_date = str(datetime.now())[0:10]
        self.list_files = set()
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('drive', 'v3', credentials=creds)

    def list_folder_contents(self, folder_id):
        query = f"'{folder_id}' in parents"
        results = self.service.files().list(
            q=query,
            pageSize=1000,
            fields="nextPageToken, files(name, id, modifiedTime, mimeType, size)",
        ).execute()
        return results.get('files', [])

    def fetch_files(self, folder_id):
        folder_contents = self.list_folder_contents(folder_id)
        for item in folder_contents:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                self.fetch_files(item['id'])
            else:
                self.list_files.add((item['name'], item['id'], item['modifiedTime'][0:10]))

    def fetch_files_today(self):
        today_files = set()
        for item in self.list_files:
            if item[2] == self.today_date:
                today_files.add((item[0], item[1], item[2]))
        return today_files

    def read_pdf(self, pdf_name):
        pdf_path = f"todays_pdf/{pdf_name}"
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages[-3:]:
                text += page.extract_text() + "\n"
        return text

    def download_file(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        file_path = os.path.join("todays_pdf", file_name)
        with open(file_path, "wb") as f:
            f.write(request.execute())
        print(f"File {file_name} downloaded to todays_pdf folder!")

    def download_todays_files(self, root_folder_id):
        self.fetch_files(root_folder_id)
        todays_files = self.fetch_files_today()
        for file in todays_files:
            self.download_file(file[1], file[0])

# Example usage:
# pdf_manager = PDFDriveManager()
# pdf_manager.download_todays_files("10Uq_yUucXbMURhhFUDN73Y9PwikEQ0gX")
# text = pdf_manager.read_pdf("example.pdf")



