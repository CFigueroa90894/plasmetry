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
    
    """GoogleDrive is defined to act as the interface for communication with the Google Drive Client. """
    
    def __init__(self, text_out, credentials_path='', folder_id=''):
        
        """Offsite wrapper constructor."""
        
        self.say = text_out
        self.credentials_path = credentials_path
        self.validate_path(credentials_path)
        
        
        # Parent folder ID, extracted from URL of the google drive folder
        self.parent_folder = folder_id
    
            
    def validate_path(self, credentials_path):
        
        """Returns boolean value validating the received path. Also sets the path if valid."""

        # Check if the directory exists 
        if  os.path.exists(credentials_path):
            # Set the path for local storage
            self.credentials_path = credentials_path
            
            # Storing credentials object, used to authenticate API requests
            self.creds = self.authenticate_connection()
            if self.creds:
                return True
        else:
            self.credentials_path= ''
        
    def validate_connection(self):
        
        """Internet connection validation, returns True if connection valid, False if otherwise."""
        # Storing port for communication, in this case for https traffic
        PORT = 443
        # Verifying that the connection to googleapis.com may be established
        try:
            #
            socket.getaddrinfo('googleapis.com', PORT)
            return True
        
        # Error handling if socket.gaierror is raised
        # Usually raised due to network issues, DNS problems 
        # and firewall or proxy settings that block the request
        except socket.gaierror as er:
            self.say(f'{er}: Cannot connect to Google Drive. Verify your internet connection')
            return None
            
    def authenticate_connection(self):
        
        """Returns either a credentials object used for Google Drive API authentication
        
        or an empty string."""
        
        # Scope of the account (TEMPORARY PLACE, WILL REMOVE)
        SCOPES = ['https://www.googleapis.com/auth/drive']
        
        try:
            # Storing the credentials object
            creds = service_account.Credentials.from_service_account_file(self.credentials_path, scopes=SCOPES)
        except Exception as e:
            self.say(e)
            creds = ''
       
        # Returning the credentials object
        return creds

    def put_request(self, csv_obj, file_name):

        """Uploads data to google drive folder"""
        if self.creds:
            # Object used to interact with the Google Drive API
            service = build('drive', 'v3', credentials= self.creds)

            # File metadata, must be defined as such to use service.files().create
            file_metadata = {
            'name':file_name,
            'parents':[self.parent_folder],
            'mimeType':'text/csv'
             }
           
            # Encoding the csv to a bytes-like object, necessary to invoke MediaIoBaseUpload 
            encoded_data= csv_obj.encode('utf-8')
            
            # Creating csv media object from the endoded data
            media = MediaIoBaseUpload(io.BytesIO(encoded_data), mimetype='text/csv', resumable=True)
            
            # Uploading the csv media object, must be invoked as such to execute the upload
            file = service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()
            
    def folder_exists(self, folder_name):
        """Check if the folder exists in the Google Drive. 
        
        If so, changes upload location to that folder and returns True."""
        
        # instantiating object used to interact with the Google Drive API
        service = build('drive', 'v3', credentials=self.creds)
        
        # Query that verifies in the parent folde if the folder already exists
        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and '{self.parent_folder}' in parents and trashed=false"
        
        # Invoking query and storing in results variable
        results = service.files().list(
            q=query,
            fields="files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        
        # Storing query filenames in a list called items
        items = results.get('files', [])
        
        # Verifying if items is not empty. If not, setting the folder name as the new upload location
        if items:
            # Setting the identified folder's id as the new upload location
            self.set_folder_id(items[0]['id'])
            # Return True to continue operations and notify that the folder must not be created
            return True
        else:
            # Return False, since the folder must be created
            return False

    def create_folder(self, folder_name):
        """Create a new folder in Google Drive."""
        # instantiating object used to interact with the Google Drive API

        service = build('drive', 'v3', credentials=self.creds)
        
        # New folder metadata, used for API query
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.parent_folder]  
        }
        
        # Invoking create request through Google Drive API and storing the info of the new folder 
        folder = service.files().create(
            body=file_metadata,
            fields='id',
            supportsAllDrives=True
        ).execute()
        
        # Storing the new id for storage
        self.set_folder_id(folder.get('id'))
         
    def set_folder_id(self, folder_id):
        
            """Sets the id of folder for storage."""
            
            self.parent_folder = folder_id

