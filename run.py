# coding=utf-8


from Baibako import Baibako

"""
Логин
"""
username = "your_username_here"

"""
Пароль
"""
password = "your_password_here"

"""
URL RSS-ленты.

Ссылку на ленту нужно сформировать с параметрами:
    Тип ссылки в RSS: Ссылка на скачивание
    Тип логина: Альтернативный (passkey)
"""
rss_url = "http://baibako.tv/rss.php?feed=dl&cat=aa,bb,cc,dd&passkey=your_passkey"

"""
Директория автодобавления торрентов вашего торрент-клиента.
"""
#watch_directory = "D:/"
watch_directory = "/storage/downloads/watch/"

"""
Фильтр по расширениям.
"""
#extension_filter = ["avi", "mp4", "mkv"]
#extension_filter = ["mp4", "mkv"]
extension_filter = ["mkv"]

Baibako(username, password, rss_url, watch_directory, extension_filter).parse()