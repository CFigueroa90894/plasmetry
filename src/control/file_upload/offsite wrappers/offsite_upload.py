""" G3 - Plasma Devs
Layer 2 - Control - Offsite Upload
    This module specifies the interface for wrappers used to upload a remote storage service.

author: <----------------------
status: <?>

Classes:
    OffsiteUpload

"""


from abc import ABC, abstractmethod

class OffsiteUpload(ABC):
    """This abstract class specifies five methods that concrete wrapper for remote storage upload
    in order to be comptatible with the FilUpload module.
    
    Methods:
        + authenticate_connection()
        + put_request()
        + validate_connection()
        + create_folder()
        + folder_exists()
    """
    
    @abstractmethod
    def authenticate_connection(self):
        
        """Authentication must be implemented here"""
        raise NotImplementedError
        
    @abstractmethod
    def put_request(self):
        
        """Off-site file uploads must be implemented here"""
        
        raise NotImplementedError
        
    @abstractmethod
    def validate_connection(self):
        
        raise NotImplementedError
        
    @abstractmethod
    def create_folder(self):
        
        raise NotImplementedError
        
    @abstractmethod
    def folder_exists(self):
        
        raise NotImplementedError
    
    
