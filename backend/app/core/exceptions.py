class CustomException(Exception):
    """Base class for custom exceptions in the application."""
    pass

class DocumentUploadException(CustomException):
    """Exception raised for errors in document uploads."""
    def __init__(self, message="Error uploading document."):
        self.message = message
        super().__init__(self.message)

class DocumentProcessingException(CustomException):
    """Exception raised for errors in document processing."""
    def __init__(self, message="Error processing document."):
        self.message = message
        super().__init__(self.message)

class ChatInteractionException(CustomException):
    """Exception raised for errors during chat interactions."""
    def __init__(self, message="Error during chat interaction."):
        self.message = message
        super().__init__(self.message)