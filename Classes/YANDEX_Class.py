import requests


class YaUploader:

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {"Content-Type": "application/json",
                "Authorization": f"OAuth {self.token}"}

    def get_folder(self, path_folder):
        url_folder = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        response = requests.put(f"{url_folder}?path={path_folder}", headers=headers)
        if response.status_code == 201:
            print(f"Папка {path_folder} создана.")
        else:
            response.raise_for_status()
            if response.status_code == 409:
                print(f"Папка {path_folder} уже существует! Введите другое название.")

    def upload_files_to_disk(self, path_folder, photo_url):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        upload_params = {"path": path_folder, "url": photo_url}
        response = requests.post(url=upload_url, params=upload_params, headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print("Загрузка файла(-ов) завершена")
