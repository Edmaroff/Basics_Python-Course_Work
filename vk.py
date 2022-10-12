import requests
from tqdm import tqdm


class VkDownload:

    def __init__(self, token_vk):
        self.token_vk = token_vk

    # Запрос для получения словаря со всеми фотографиями пользователя
    def requests_user_photo(self, user_id, count, album_id):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': self.token_vk,
            'owner_id': user_id,
            'extended': 1,
            'album_id': album_id,
            'count': count,
            'v': 5.131
        }
        response = requests.get(url, params=params).json()
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
            'access_token': self.token_vk,
            'owner_id': user_id,
            'v': 5.131
        }
        response = requests.get(url, params=params).json()
        album_dictionary = {}
        for album_data in response['response']['items']:
            album_dictionary.update({album_data['title']: album_data['id']})
        return album_dictionary
