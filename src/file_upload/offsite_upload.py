from abc import ABC, abstractmethod

class OffsiteUpload(ABC):
    
    @abstractmethod
    def authenticate_connection(self):
        
        """Authentication must be implemented here"""
        raise NotImplementedError
        
    @abstractmethod
    def put_request(self):
        
        """Off-site file uploads must be implemented here"""
        
        raise NotImplementedError

    
    
