import os
from azure.storage.file import FileService

class Storage:
    """Manages connecting to Azure Files."""

    def __init__(self):
        # Get the variables we need
        self.account_name = os.environ.get("AZURE_ACCOUNT_NAME")
        self.account_key = os.environ.get("AZURE_ACCOUNT_KEY")
        self.azure_file_share = os.environ.get("AZURE_FILE_SHARE")

        # Handles the connection to Azure Files
        self.file_service = FileService(account_name, account_key)

        # Produces a stream of the files
        self.files_generator = self.file_service.list_directories_and_files(self.azure_file_share)

    def list_all_files(self):
        files = [f for f in self.files_generator]
        return files

    def download_file(self, filename, directory="./"):
        self.file_service.get_file_to_path(self.azure_file_share, None, filename, directory+"/"+filename)
