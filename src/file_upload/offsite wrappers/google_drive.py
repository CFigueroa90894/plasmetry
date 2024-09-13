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

import socket
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from offsite_upload import OffsiteUpload



class GoogleDrive(OffsiteUpload):
    
    def __init__(self, credentials_path='client_secrets.json'):
        
        """Offsite wrapper constructor"""
        
        # Storing the path to Google API credentials file
        self.credentials_path = credentials_path
        
        # Storing credentials object, used to authenticate API requests
        self.creds = self.authenticate_connection()
        
        # Storing port for https traffic
        self.port= 443
        
    def valid_internet_connection(self):
        
        """Internet connection with googleapis.com validation"""
        
        # Verifying that the connection may be established
        try:
            #
            socket.getaddrinfo('googleapis.com', self.port)
            return True
        
        # Error handling if socket.gaierror is raised
        # Usually raised due to network issues, DNS problems 
        # and firewall or proxy settings that block the request
        except socket.gaierror:
            print('Cannot connect to Google Drive. Verify your internet connection')
            return None
            
    def authenticate_connection(self):
        
        """Returns credentials object used for authentication."""
        
        # Scope of the account (TEMPORARY PLACE, WILL REMOVE)
        SCOPES = ['https://www.googleapis.com/auth/drive']
        
        # Storing the credentials object
        creds = service_account.Credentials.from_service_account_file(self.credentials_path, scopes=SCOPES)
        
        # Returning the credentials object
        return creds

    def put_request(self, csv_obj, file_name):
        
        """Uploads data to google drive folder"""
        
        # Parent folder ID, extracted from URL of the google drive folder
        PARENT_FOLDER_ID = "17q9inqrXiG9TSLRkPErM5993wsiBJj5i"
        
        # Object used to interact with the Google Drive API
        service = build('drive', 'v3', credentials= self.creds)

        # File metadata, must be defined as such to use service.files().create
        file_metadata = {
            'name' : file_name,
            'parents' : [PARENT_FOLDER_ID],
            'mimeType': 'text/csv'
        }
       
        # Encoding the csv to a bytes-like object, necessary to invoke MediaIoBaseUpload 
        encoded_data= csv_obj.encode('utf-8')
        
        # Creating csv media object from the endoded data
        media = MediaIoBaseUpload(io.BytesIO(encoded_data), mimetype='text/csv', resumable=True)
        
        # Uploading the csv media object, must be defined as such to execute the uplaod
        file = service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
        
    

