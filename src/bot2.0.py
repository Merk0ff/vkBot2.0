#!/usr/bin/env python

# Simply trolling made just for fun usage: just run

import sys
import os
import getpass
import time
import json
import requests
from itertools import cycle
import vk_api
import dvach_handle as ch


__author__ = "Dukshtau Philip"
__copyright__ = "Copyright 2018, The vkBot2.0 Project"
__credits__ = ["Dukshtau Philip"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "Dukshtau Philip"
__email__ = "f.dukshtau@gmail.com"
__status__ = "Release"


def list_to_str(data) -> str:
    """Create string from list.

        Create string such as: "1,2,3,4" from [1, 2, 3, 4] list

        Args:
            data: list.

        Returns:
            A string
        """
    string = str()

    for i in data:
        string += str(i) + ","

    string = string[:-1]

    return string


def load_info_json() -> dict:
    """Load 'info.json'.

        Load file that contains chat id's, groups domains and messages

        Args:
            None.

        Returns:
            A dict that contains rooms, ids, messages
        """

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    arr = {}

    # try:
    #     f = open(os.path.join(__location__, 'info.json'), "r")
    # except BaseException as err:
    #     print("File protected.json not found " + str(err))
    #     exit(0)
    #
    # arr = json.load(f)
    #
    # f.close()

    with open(os.path.join(__location__, 'info.json'), "r") as f:
        arr = json.load(f)

    return arr


def get_pick_from_wall(vk, domain, offset):
    """Get picture from domain.

        Get pictures of wall post from group by it domain

        Args:
            vk: vk api handle module.
            domain: domain, from where we going pool images
            offset: offset of posts in domain wall

        Returns:
            A list of strings, that contains vkApi links to photos
        """

    wall = vk.wall.get(domain=domain, offset=offset, count=1)['items'][0]
    photos = []

    if 'photo' not in wall['attachments'][0]:
        return None

    for i in wall['attachments']:
        owid = str(i['photo'].get('owner_id'))
        id = str(i['photo'].get('id'))
        acces = str(i['photo'].get('access_key'))

        photos.append('photo' + owid + '_' + id + '_' + acces)

    return photos


def send_message(vk, **data):
    """Send message to vk conversation.

        Send message, that can include text or text and attachments

        Args:
            vk: vk api handle module.
            Keyword Args:
                required args:
                    chat_id/user_id (str): group chat id, where to sand message/user id, where message will be sand
                    message (str): message that will be sand
                extra:
                    attachments (str): attachments list

        Returns:
            A list of strings, that contains vkApi links to photos

        Raises:
        Exception: incorrect kwargs list.

       """
    if len(data) < 1:
        return

    elif len(data) == 2:
        if "chat_id" in data:
            vk.messages.send(chat_id=data["chat_id"], message=data["message"])
        elif "user_id" in data:
            vk.messages.send(user_id=data["user_id"], message=data["message"])

    elif len(data) == 3 and "attachments" in data:
        if "chat_id" in data:
            vk.messages.send(chat_id=data["chat_id"], message=data["message"], attachment=data["attachments"])
        elif "user_id" in data:
            vk.messages.send(user_id=data["user_id"], message=data["message"], attachment=data["attachments"])
    else:
        raise Exception("Incorrect function call")


def get_vk_api():
    """Get vk api.

        Simply use vk_api module to get vkApi instance

        Args:
            None.

        Returns:
            A tuple where first: vkApi, second: token

       """
    login = input('Login:')
    password = getpass.getpass('Password:')

    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        exit(0)

    return vk_session.get_api(), vk_session.token['access_token']


def get_user_idis(vk, chat_id):
    ids = vk.messages.getChat(chat_id=chat_id)['users']
    return ids


def create_mem_party(vk, user_ids):
    """Create new conversation with user ids.

        Args:
            vk: vk api handle module.
            user_ids: string of user ids

        Returns:
            Chat id
       """

    chat_id = vk.messages.createChat(user_ids=user_ids, title='мемная вечеринка')
    send_message(vk, chat_id=chat_id, message='юху мемная вечеринка')

    return chat_id


def get_users_domains(vk, chat_id):
    """Get domains of users in conversation.

        Get domains of all users in conversation by chat_id

        Args:
            vk: vk api handle module.
            chat_id: id of chat, where fuction get ids

        Returns:
            A list of strings, that contains domains of all users in group chat
       """
    ids = get_user_idis(vk, chat_id)
    ids_str = list_to_str(ids)

    domains = vk.users.get(user_ids=ids_str, fields="domain")
    domains_list = []

    for d in domains:
        domains_list.append(d['domain'])

    return domains_list


def wake_up(vk, chat_id, domains):
    """Just funny function that mention everyone in group chat.

        Args:
            vk: vk api handle module.
            chat_id: id of chat, where it will do fun
            domains: a list of domains, use - get_users_domains() to get it

        Returns:
           None.
       """
    message = ""
    for d in domains:
        message += "@" + str(d) + " "

    message = message[:-1]

    send_message(vk, chat_id=chat_id, message=message)


def upload_pick(vk, files):
    """Upload picks to message attachments.

        Args:
            vk: vk api handle module.
            files: list of file names

        Returns:
           list of attachments.
       """
    att_link = []

    for file in files:
        upload_url = vk.photos.getMessagesUploadServer()['upload_url']

        with open(file, 'rb') as f:
            file_id = requests.post(upload_url, files={'photo': f})

        if file_id.status_code != 200:
            return

        file_id = json.loads(file_id.text)
        link = vk.photos.saveMessagesPhoto(photo=file_id['photo'], server=file_id['server'], hash=file_id['hash'])

        att_link.append('photo' + str(link[0]['owner_id']) + '_' + str(link[0]['id']))

    return att_link


def main():
    FNAME = "key.txt"
    vk, token = get_vk_api()
    key = 2
    info = load_info_json()
    count_of_sended = 0
    # create 2ch object
    d_api = ch.DvachHandle("https://2ch.hk/b/res/186610524.html", 60)


    domain = info['domain']
    messages = info['messages']
    chat_ids_begin = info['chat_ids']
    chat_ids = []

    # create new chat with users from chats that contains in info.json
    for chat in chat_ids_begin:
        chat_ids.append(str(create_mem_party(vk, list_to_str(get_user_idis(vk, chat)))))


    if os.path.isfile(FNAME):
        with open(FNAME, "r") as f:
            k = f.readline()
            if k != '':
                key = int(k)

    domain_cycle = cycle(domain)
    message_cycle = cycle(messages)

    # wake up function call

    # for room in chat_ids:
    #     send_message(vk, chat_id=room, message="Поїхали")
    #     domains_list = get_users_domains(vk, room)
    #     wake_up(vk, room, domains_list)
    #     time.sleep(0.5)

    while 1:
        urls = upload_pick(vk, d_api.get_images())

        att = list_to_str(urls) # list_to_str(get_pick_from_wall(vk, next(domain_cycle), key))
        msg = next(message_cycle)  # + " @" + random.choice(domains_list)

        # if att is None:
        #     key += 1
        #     continue

        for room in chat_ids:
            send_message(vk, chat_id=room, message=msg, attachments=att)
            time.sleep(0.5)

        key += 1
        count_of_sended += 1

        print("You sanded: " + str(count_of_sended) + " posts \r", sep=' ', end='', flush=True)

        with open(FNAME, "w") as f:
            f.write(str(key))

        time.sleep(5)


if __name__ == '__main__':
    main()
