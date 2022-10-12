import requests
from tqdm import tqdm


class YandexDisk:

    def __init__(self, token_yd):
        self.token_yd = token_yd

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token_yd}'
        }

    # Загрузить фото на ЯД, принимая ссылку на файл - download_link, имя созданной папки - name_folder и
    # путь на диске - path_in_disk
    def upload_photo_in_disk(self, name_folder, path_in_disk, download_link):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {
            'fields': "file_name",
            'path': f'{name_folder}/{path_in_disk}',
            'url': download_link,
        }
        response = requests.post(url, headers=headers, params=params)

    # Создать папку с выбранным названием name_folder
    def create_folder(self, name_folder):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {
            'path': name_folder,
        }
        response = requests.put(url, headers=headers, params=params)
        return response

    # Загрузка фото в ЯД
    def upload_list_photos(self, dict_data_photos, name_folder):
        self.create_folder(name_folder)
        for info_photo in tqdm(dict_data_photos.values(), desc='Загрузка фотографий на Яндекс Диск'):
            for name, link in info_photo.items():
                self.upload_photo_in_disk(name_folder, name, link)
