import io, os
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import shutil
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
from . import general_operand


class Google:
    def __init__(self):
        #gauth = GoogleAuth()
        #gauth.LocalWebserverAuth()

        #self.drive = GoogleDrive(gauth)

        SCOPES = ['https://www.googleapis.com/auth/drive']

        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json', SCOPES)
                creds = flow.run_local_server(port=8000)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        global service, access_token
        self.service = build('drive', 'v3', credentials=creds)



    def list_content(self):

        file_list = self.drive.ListFile({'q': ""}).GetList()
        for file1 in file_list:
            print(file1['title'], file1['id'])

    def uploader(self, file, name):

        metadata = {'name': name, 'parents':["1_Az5T_cOlt7YL0RVbWFEnwk89EtHBO2i"]}
        media_body = MediaFileUpload(file, resumable=True)
        res = self.service.files().create(body=metadata, media_body=media_body).execute()
        res["size"]=str(os.path.getsize(file)/1000000)+" MB"
        return res

    def delete(self, file_id):
        self.service.files().delete(fileId=file_id).execute()





