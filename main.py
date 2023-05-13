from random import randint
from urllib.parse import urlparse, unquote
import os

from dotenv import load_dotenv
import requests


def check_for_vk_errors(feedback):
    if 'error' in feedback:
        raise requests.HTTPError(feedback['error'])


def get_last_comics_number():
    link = 'https://xkcd.com/info.0.json'
    response = requests.get(link)
    response.raise_for_status()
    deserialized_response = response.json()
    num = deserialized_response['num']
    return num


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


def get_address_to_upload(token, version):
    link = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'v': version,
    }
    response = requests.get(link, params=params)
    response.raise_for_status()
    deserialized_response = response.json()
    check_for_vk_errors(deserialized_response)
    return deserialized_response['response']['upload_url']


def upload_picture(address, file_name):
    with open(file_name, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(address, files=files)
    response.raise_for_status()
    deserialized_response = response.json()
    check_for_vk_errors(deserialized_response)
    return deserialized_response


def save_wall_photo(server, photo, hash_photo, token, version):
    params = {
        'server': server,
        'photo': photo,
        'hash': hash_photo,
        'access_token': token,
        'v': version,
    }
    link = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(link, params=params)
    response.raise_for_status()
    deserialized_response = response.json()
    check_for_vk_errors(deserialized_response)
    vk_response = deserialized_response['response'][0]
    owner_id = vk_response['owner_id']
    photo_id = vk_response['id']
    return f'photo{owner_id}_{photo_id}'


def post_on_wall(community_id, saved_photo, alt, token, version):
    saved_photo_data = {
        'owner_id': f'-{community_id}',
        'attachments': saved_photo,
        'message': alt,
        'access_token': token,
        'v': version,
    }
    link = 'https://api.vk.com/method/wall.post'
    response = requests.post(link, params=saved_photo_data)
    response.raise_for_status()
    deserialized_response = response.json()
    check_for_vk_errors(deserialized_response)


def main():
    total_comics_number = get_last_comics_number()
    comics_num = randint(1, total_comics_number)
    file_name, alt = download_python_comics(comics_num)
    try:
        load_dotenv()
        token = os.environ['VK_TOKEN']
        version = os.environ['API_VERSION']
        community_id = os.environ['COMMUNITY_ID']
        address_to_upload = get_address_to_upload(token, version)
        uploaded_photo_data = upload_picture(address_to_upload, file_name)
        saved_photo = save_wall_photo(
            uploaded_photo_data['server'],
            uploaded_photo_data['photo'],
            uploaded_photo_data['hash'],
            token,
            version,
        )
        post_on_wall(community_id, saved_photo, alt, token, version)
    finally:
        os.remove(file_name)


if __name__ == '__main__':
    main()
