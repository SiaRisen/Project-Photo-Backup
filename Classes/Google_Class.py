from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
import requests
import io

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = " "  # путь к файлу с ключами сервисного аккаунта


class GoogleUploader:

    """Класс для загрузки фото на Google.Drive"""
    
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('drive', 'v3', credentials=credentials)

    def get_folder(self, name):
        file_metadata = {'name': name,
                         'mimeType': 'application/vnd.google-apps.folder'}
        response = self.service.files().create(body=file_metadata, fields='id').execute()
        if response.status_code == 201:
            print(f"Папка {name} создана.")
        else:
            response.raise_for_status()
            print("Ошибка")

    def upload_files_to_disk(self, folder_id, photos_list):
        info = requests.get(photos_list['url'])
        file_content = io.BytesIO(info.content)
        file_metadata = {'name': f"{photos_list['file_name']}", 'parents': [folder_id]}
        media = MediaIoBaseUpload(file_content, mimetype='image/jpeg')
        response = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        response.raise_for_status()
        if response.status_code == 201:
            print("Загрузка файла(-ов) завершена")
        else:
            response.raise_for_status()
            print("Ошибка")
