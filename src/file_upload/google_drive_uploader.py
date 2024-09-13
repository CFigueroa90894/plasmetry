import os
import sys
# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 1           # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
   # print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

from googleapiclient.discovery import build
from google.oauth2 import service_account
from offsite_upload import OffsiteUpload

class GoogleDriveUpload(OffsiteUpload):
    
    def __init__(self, credentials_path='client_secrets.json'):
        
        OffsiteUpload.credentials_path = credentials_path
        self.authenticate_connection()
    
    def authenticate_connection(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = service_account.Credentials.from_service_account_file(self.credentials_path, scopes=SCOPES)
        return creds

    def put_request(self, file_path):
        PARENT_FOLDER_ID = "17q9inqrXiG9TSLRkPErM5993wsiBJj5i"
        creds = self.authenticate_connection()
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name' : "Demonstration",
            'parents' : [PARENT_FOLDER_ID]
        }

        file = service.files().create(
            body=file_metadata,
            media_body=file_path
        ).execute()
        
if __name__ == "__main__": 
     uploader = GoogleDriveUpload('C:/Users/ajco2/Downloads/plasma-software-data-upload-d6f40f4fefdc.json')
     uploader.put_request('testing path/testing 2024-09-12 parameters.csv')
