from vk import VkDownload
from YandexDisk import YandexDisk
import json


# Запись информации о загруженных фото в файл .json
def writing_to_file(dict_data_photos):
    list_data_photos = []
    for size, name_and_link in dict_data_photos.items():
        for name in name_and_link:
            list_data_photos.append({'file_name': f'{name}.jpg', 'size': f'{size} B'})
    with open("upload_info.json", "w") as file:
        json.dump(list_data_photos, file, indent=4)

# Работа кода, если загружаем фотографии со страницы пользователя
def information_output_avatar(user_id, instance_vk, instance_yd):
    count = int(input('Сколько фотографий вы хотите скачать? '))
    dict_data_photos = instance_vk.get_dict_info_photos(user_id, count)
    name_folder = input('Введите название папки для загрузки: ')
    instance_yd.upload_list_photos(dict_data_photos, name_folder)
    writing_to_file(dict_data_photos)
    print(f'{len(dict_data_photos)} фото установлены на ЯД, информация о них содержится в файле "upload_info.json".')

# Работа кода, если загружаем фотографии с альбомов пользователя
def information_output_album(user_id, instance_vk, instance_yd):
    album = instance_vk.requests_user_albums(user_id)
    if len(album) == 0:
        print('У пользователя нет альбомов.')
    else:
        print(f'Список альбомов пользователя: {list(album.keys())}')
        album_name = input('Введите название альбома из которого вы хотите скачать фотографии: ')
        album_id = album[album_name]
        count = int(input('Сколько фотографий вы хотите скачать? '))
        dict_data_photos = vk.get_dict_info_photos(user_id, count, album_id)
        name_folder = input('Введите название папки для загрузки: ')
        instance_yd.upload_list_photos(dict_data_photos, name_folder)
        writing_to_file(dict_data_photos)
        print(f'{len(dict_data_photos)} фото установлены на ЯД в папку {name_folder}, информация о них содержится в '
              f'файле "upload_info.json".')


# ID пользователей для проверки работы программы:
# 1) 225325935 - одинаковое кол-во лайков на 2ух фото
# 2) 11524647 - у пользователя 7 альбомов
if __name__ == '__main__':
    token_vk = ' '
    token_yd = ' '
    vk = VkDownload(token_vk)
    yd = YandexDisk(token_yd)
    user_id = input('Введите ID пользователя: ')
    avatar = input('Вы хотите скачать фотографии с профиля пользователя? ')
    if avatar == 'да':
        information_output_avatar(user_id, vk, yd)
    if avatar == 'нет':
        information_output_album(user_id, vk, yd)


