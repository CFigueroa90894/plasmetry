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
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from offsite_upload import OffsiteUpload
import socket




class GoogleDrive(OffsiteUpload):
    
    def __init__(self, credentials_path='client_secrets.json'):
        
        """"""
        
        self.credentials_path = credentials_path
        self.creds = self.authenticate_connection()
        self.port= 443
        
    def valid_internet_connection(self):
        
        """"""
        
        try:
            socket.getaddrinfo('google.com', self.port)
            return True
        except socket.gaierror:
            print('Cannot connect to Google.com, verify your internet connection.')
            return None
            
    def authenticate_connection(self):
        
        """"""
        
        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = service_account.Credentials.from_service_account_file(self.credentials_path, scopes=SCOPES)
        return creds

    def put_request(self, csv_obj, file_name):
        
        """"""
        
        PARENT_FOLDER_ID = "17q9inqrXiG9TSLRkPErM5993wsiBJj5i"
        service = build('drive', 'v3', credentials= self.creds)

        file_metadata = {
            'name' : file_name,
            'parents' : [PARENT_FOLDER_ID],
            'mimeType': 'text/csv'
        }
       
        media = MediaIoBaseUpload(io.BytesIO(csv_obj.encode('utf-8')), mimetype='text/csv', resumable=True)
        
        file = service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
        
    

