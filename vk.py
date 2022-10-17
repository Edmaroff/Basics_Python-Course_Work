import requests
from tqdm import tqdm


class VkDownload:

    def __init__(self, token_vk):
        self.token_vk = token_vk

    def get_params(self):
        return {
            'access_token': self.token_vk,
            'v': 5.131,
        }

    # Запрос для получения id пользователя, зная username
    def get_id_user(self, username):
        url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': username,
        }
        response = requests.get(url, params=params | self.get_params()).json()
        return ((response['response'])[0])['id']

    # Запрос для получения словаря со всеми фотографиями пользователя
    def requests_user_photo(self, user_id, count, album_id):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': user_id,
            'extended': 1,
            'album_id': album_id,
            'count': count,
        }
        response = requests.get(url, params=params | self.get_params()).json()
        return response['response']['items']

    # Получение размера фото, зная URL
    def get_size(self, url):
        res = requests.get(url).headers['Content-Length']
        return int(res)

    # Получение словаря со ссылками на фото {лайки: {размер фото: ссылка}}, на вход результат запроса HTTP
    def get_photos_in_album(self, query_result):
        photo_dictionary = {}
        for photo_data in tqdm(query_result, desc='Обработка информации о фотографиях'):
            if photo_data['likes']['count'] not in photo_dictionary:
                key = photo_dictionary[photo_data['likes']['count']] = {}
            else:
                key = photo_dictionary[f"{photo_data['likes']['count']}_{photo_data['id']}"] = {}
            for photo in photo_data['sizes']:
                key.update({self.get_size(photo['url']): photo['url']})
        return photo_dictionary

    # Получение словаря {максимальный размер: {имя файла: ссылка на фото}
    def get_dict_info_photos(self, user_id, count=5, album_id='profile'):
        query_result = self.requests_user_photo(user_id, count, album_id)
        dictionary = self.get_photos_in_album(query_result)
        dict_info_photos = {}
        for names, size_and_links in dictionary.items():
            for size, link in size_and_links.items():
                if size == max(size_and_links):
                    dict_info_photos[size] = {names: link}
        return dict_info_photos

    # РАБОТА С АЛЬБОМАМИ ПОЛЬЗОВАТЕЛЯ
    # Получение словаря {Название альбома: ID альбома}
    def requests_user_albums(self, user_id=11524647):
        url = 'https://api.vk.com/method/photos.getAlbums'
        params = {
            'owner_id': user_id,
        }
        response = requests.get(url, params=params | self.get_params()).json()
        album_dictionary = {}
        for album_data in response['response']['items']:
            album_dictionary.update({album_data['title']: album_data['id']})
        return album_dictionary

    # Работа кода, если загружаем фотографии со страницы пользователя
    def information_output_avatar(self, user_id, instance_yd):
        count = int(input('Сколько фотографий вы хотите скачать? '))
        dict_data_photos = self.get_dict_info_photos(user_id, count)
        name_folder = input('Введите название папки для загрузки: ')
        instance_yd.upload_list_photos(dict_data_photos, name_folder)
        from main import writing_to_file
        writing_to_file(dict_data_photos)
        print(f'{len(dict_data_photos)} фото установлены на ЯД, информация о них содержится в файле "upload_info.json".')

    # Работа кода, если загружаем фотографии с альбомов пользователя
    def information_output_album(self, user_id, instance_yd):
        album = self.requests_user_albums(user_id)
        if len(album) == 0:
            print('У пользователя нет альбомов.')
        else:
            print(f'Список альбомов пользователя: {list(album.keys())}')
            album_name = input('Введите название альбома из которого вы хотите скачать фотографии: ')
            album_id = album[album_name]
            count = int(input('Сколько фотографий вы хотите скачать? '))
            dict_data_photos = self.get_dict_info_photos(user_id, count, album_id)
            name_folder = input('Введите название папки для загрузки: ')
            instance_yd.upload_list_photos(dict_data_photos, name_folder)
            from main import writing_to_file
            writing_to_file(dict_data_photos)
            print(f'{len(dict_data_photos)} фото установлены на ЯД в папку {name_folder}, информация о них содержится в '
                  f'файле "upload_info.json".')
