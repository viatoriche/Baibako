# coding=utf-8


import os
import urllib
import urllib2
import cookielib
import xml.etree.ElementTree
import datetime
import random
import re


class Baibako:
    """
    Baibako торрент-парсер.

    @author Werner van Croy <mail@vancroy.ru>
    @version 0.31
    @date 2013/04/28
    """

    _username = ""
    _password = ""
    _rss_url = ""
    _watch_directory = ""
    _re_filter = ""

    _user_agent = "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"
    _save_file = "Baibako.txt"

    _save_file_max_lines_count = 100
    _error_string = ["<html", "Fatal error"]

    _cookie_jar = None


    def _torrent_url_adaptation(self, torrent_url):
        """
        Постобработка ссылок.
        """

        return torrent_url.replace(" ", ".")


    def _filter_torrent_url_by_re(self, torrent_url):
        """
        Отфильтровать ссылки по регулярному выражению.
        """

        try:
            if re.search(self._re_filter, torrent_url):
                return True
        except Exception as e01:
            return False

        return False


    def _check_for_errors(self, text):
        """
        Отфильтровать ошибочные загрузки.
        """

        for error in self._error_string:
            if error in text:
                return True

        return False


    def _download_torrent(self, torrent_url):
        """
        Скачать торрент.
        """

        if torrent_url == "":
            return False
        if self._watch_directory == "":
            return False
        if not os.path.exists(self._watch_directory):
            return False

        if self._cookie_jar is None:
            self._cookie_jar = cookielib.CookieJar()

            opener_director = urllib2.build_opener()
            opener_director.addheaders = [("User-Agent", self._user_agent)]
            opener_director.add_handler(urllib2.HTTPCookieProcessor(self._cookie_jar))
            response = opener_director.open("http://baibako.tv/takelogin.php",
                urllib.urlencode({"username": self._username, "password": self._password}))

        opener_director = urllib2.build_opener()
        opener_director.addheaders = [("User-Agent", self._user_agent)]
        opener_director.add_handler(urllib2.HTTPCookieProcessor(self._cookie_jar))

        try:
            response = opener_director.open(torrent_url).read()
        except ValueError as e01:
            return False

        if self._check_for_errors(response):
            return False

        try:
            text_file = open(self._watch_directory + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(
                random.randint(1000, 9999)) + ".torrent", "wb")
        except IOError as e02:
            return False

        text_file.write(response)
        text_file.close()

        return True


    def _save_torrent_url_list(self, torrent_url_list):
        """
        Сохранить список ссылок в файл.
        """

        file = open(self._save_file, "w")

        counter = self._save_file_max_lines_count
        if len(torrent_url_list) < self._save_file_max_lines_count:
            counter = len(torrent_url_list)

        for i in range(0, counter):
            file.write(torrent_url_list[i] + "\n")


    def _get_saved_torrent_url_list(self):
        """
        Получить список ссылок из файла.
        """

        try:
            file = open(self._save_file, "r")
        except IOError as e01:
            file = open(self._save_file, "w")
            file.close()
            file = open(self._save_file, "r")

        for torrent_url in file.readlines():
            torrent_url_striped = torrent_url.strip(" \t\n\r")
            if torrent_url_striped != "":
                yield torrent_url_striped


    def _get_rss_torrent_url_list(self):
        """
        Получить список ссылок из RSS.
        """

        if self._cookie_jar is None:
            self._cookie_jar = cookielib.CookieJar()

            opener_director = urllib2.build_opener()
            opener_director.addheaders = [("User-Agent", self._user_agent)]
            opener_director.add_handler(urllib2.HTTPCookieProcessor(self._cookie_jar))
            response = opener_director.open("http://baibako.tv/takelogin.php",
                urllib.urlencode({"username": self._username, "password": self._password}))

        opener_director = urllib2.build_opener()
        opener_director.addheaders = [("User-Agent", self._user_agent)]
        opener_director.add_handler(urllib2.HTTPCookieProcessor(self._cookie_jar))

        try:
            response = opener_director.open(self._rss_url).read()
        except IOError as e01:
            return

        try:
            rss = xml.etree.ElementTree.fromstring(response)
        except xml.etree.ElementTree.ParseError as e02:
            return

        for node in rss[0]:
            if node.tag == "item":
                torrent_url = node[1].text.strip(" \t\n\r")
                if torrent_url != "":
                    yield torrent_url


    def __init__(self,
                 username="",
                 password="",
                 rss_url="",
                 watch_directory="",
                 re_filter=""):
        """
        Конструктор.
        """

        if isinstance(username, str):
            self._username = username.strip(" \t\n\r")

        if isinstance(password, str):
            self._password = password.strip(" \t\n\r")

        if isinstance(rss_url, str):
            self._rss_url = rss_url.strip(" \t\n\r")

        if isinstance(watch_directory, str):
            self._watch_directory = watch_directory.strip(" \t\n\r")

        if isinstance(re_filter, str):
            self._re_filter = re_filter.strip(" \t\n\r")


    def parse(self):
        """
        Запуск парсера.
        """

        rss_torrent_url_list = list(self._get_rss_torrent_url_list())
        saved_torrent_url_list = list(self._get_saved_torrent_url_list())

        # Обходим все полученные ссылки от поздних к ранним.
        for rss_torrent_url in reversed(rss_torrent_url_list):
            # Заменяем в ссылках неправильные символы.
            rss_torrent_url_adapted = self._torrent_url_adaptation(rss_torrent_url)
            # Проверяем соответствует ли ссылка регулярному выражению.
            if self._filter_torrent_url_by_re(rss_torrent_url_adapted):
                # Если ссылка не найдена в файле, то пытаемся скачать торрент.
                if rss_torrent_url_adapted not in saved_torrent_url_list:
                    # Если торрент успешно скачался, то заносим ссылку в файл в начало списка.
                    if self._download_torrent(rss_torrent_url_adapted):
                        saved_torrent_url_list.insert(0, rss_torrent_url_adapted)

        self._save_torrent_url_list(saved_torrent_url_list)