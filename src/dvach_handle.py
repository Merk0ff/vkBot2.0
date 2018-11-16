#!/usr/bin/env python

# 2ch module handle

from bs4 import BeautifulSoup as bs
import urllib.request as req

__author__ = "Dukshtau Philip"
__copyright__ = "Copyright 2018, The vkBot2.0 Project"
__credits__ = ["Dukshtau Philip"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "Dukshtau Philip"
__email__ = "f.dukshtau@gmail.com"
__status__ = "Release"

class DvachHandle:
    def __init__(self, thread_link: str, offset=0):
        self._thread_link = thread_link
        self._post_index = offset

        try:
            html = req.urlopen(self._thread_link, timeout=1)
        except req.URLError as e:
            print(self._thread_link + ' : ' + str(e))
            return
        try:
            self._soup = bs(html, "html.parser")
        except BaseException as e:
            print("Vse pizda: " + str(e))

        self._all_posts = self._soup.find_all(class_='images-multi')
        self._all_posts += self._soup.find_all(class_='images-single')

    def get_images(self):
        img_src = []

        try:
            images = self._all_posts[self._post_index].find_all('a', class_='desktop')

            self._post_index += 1

            for img in images:
                ex = img['href'].split('/')[-1]

                try:
                    req.urlretrieve('https://2ch.hk' + img['href'], "img/file_" + ex)
                except BaseException as e:
                    print("Some hell is going on: " + str(e))

                img_src.append("img/file_" + ex)

        except BaseException as e:
            print("Shit: " + str(e))

        return img_src


