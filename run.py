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
    Тип логина: Нет
"""
rss_url = "http://baibako.tv/rss2.php?feed=dl&cat=aa,bb,cc,dd"

"""
Директория автодобавления торрентов вашего торрент-клиента.
"""
# watch_directory = "D:/"
watch_directory = "/storage/downloads/watch/"

"""
Фильтр по регулярному выражению.
"""
# re_filter = "(mp4{1,})"  # только с расширением mp4
re_filter = "(HD1080p{1,})(.{1,})(mkv{1,})"  # только с расширением mkv и в качестве HD1080p

Baibako(username, password, rss_url, watch_directory, re_filter).parse()