# Постим комиксы в сообщество VK

* Скрипт получает рандомную картинку с сайта [xkcd](https://xkcd.com)
* Сохраняет файл
* Публикует вместе с подписью в сообществе VK
* Удаляет файл

### Как установить

1. Создать venv
```console
python3 -m venv venv
```
2. Активировать venv
```console
source venv/bin/activate
```
3. Установить зависимости
```console
pip install -r requirements.txt
```
4. Создать файл .env  
   * [Зарегистрироваться](https://api.superjob.ru/register), получить токен.
   * Создать файл
   ```console
    echo "VK_TOKEN=<Токен>" > .env
    ```
5. Запустить скрипт
```console
python3 main.py
```

### Заполнение .env

После регистрации сообщества и приложения VK, необходимо пройти процедуру [Implicit Flow](https://dev.vk.com/api/access-token/implicit-flow-user) для получения токена.  

Файл .env ожидает указания следующих переменных:
* ``VK_TOKEN``
* ``COMMUNITY_ID`` - id сообщества


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).