from vk import VkDownload
from YandexDisk import YandexDisk
import json
import configparser


# Запись информации о загруженных фото в файл .json
def writing_to_file(dict_data_photos):
    list_data_photos = []
    for size, name_and_link in dict_data_photos.items():
        for name in name_and_link:
            list_data_photos.append({'file_name': f'{name}.jpg', 'size': f'{size} B'})
    with open("upload_info.json", "w") as file:
        json.dump(list_data_photos, file, indent=4)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.ini")
    token_vk = config['VK']['token']
    token_yd = config['Yandex_Disk']['token']
    vk = VkDownload(token_vk)
    yd = YandexDisk(token_yd)
    user_id = input('Введите ID или username пользователя: ')
    if not user_id.isdigit():
        username = user_id
        user_id = vk.get_id_user(username)
    avatar = input('Вы хотите скачать фотографии с профиля пользователя? ')
    if avatar == 'да':
        vk.information_output_avatar(user_id, yd)
    if avatar == 'нет':
        vk.information_output_album(user_id, yd)

