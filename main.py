from random import randint
from urllib.parse import urlparse, unquote
import os

from dotenv import load_dotenv
import requests


def download_image(url, abs_path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(abs_path, 'wb') as file:
        file.write(response.content)


def download_python_comics(comics_num):
    link = f'https://xkcd.com/{comics_num}/info.0.json'
    response = requests.get(link)
    response.raise_for_status()
    deserialized_response = response.json()
    file_link = deserialized_response['img']
    parsed_img_url = urlparse(file_link)
    file_name = os.path.basename(unquote(parsed_img_url.path))
    alt = deserialized_response['alt']
    download_image(file_link, file_name)
    return file_name, alt


def get_address_to_upload(token):
    link = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'v': '5.124'
    }
    response = requests.get(link, params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_picture(address, file_name):
    with open(file_name, 'rb') as file:
        url = address
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
    return response.json()


def save_wall_photo(uploaded_photo_data):
    link = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(link, params=uploaded_photo_data)
    response.raise_for_status()
    response_deserialized = response.json()['response'][0]
    return (
        f"photo{response_deserialized['owner_id']}_"
        f"{response_deserialized['id']}"
    )


def wall_post(saved_photo_data):
    link = 'https://api.vk.com/method/wall.post'
    response = requests.post(link, params=saved_photo_data)
    response.raise_for_status()


def get_last_comics_number():
    link = 'https://xkcd.com/info.0.json'
    response = requests.get(link)
    response.raise_for_status()
    deserialized_response = response.json()
    num = deserialized_response['num']
    return num


def main():
    total_comics_number = get_last_comics_number()
    comics_num = randint(1, total_comics_number)
    file_name, alt = download_python_comics(comics_num)
    load_dotenv()
    token = os.getenv('VK_TOKEN')
    community_id = os.getenv('COMMUNITY_ID')
    address_to_upload = get_address_to_upload(token)
    uploaded_photo_data = upload_picture(address_to_upload, file_name)
    uploaded_photo_data['access_token'] = token
    uploaded_photo_data['v'] = '5.124'
    saved_photo = save_wall_photo(uploaded_photo_data)
    saved_photo_data = {
        'owner_id': f'-{community_id}',
        'attachments': saved_photo,
        'message': alt,
        'from_group': '1',
        'access_token': token,
        'v': '5.124'
    }
    wall_post(saved_photo_data)
    os.remove(file_name)


if __name__ == '__main__':
    main()
