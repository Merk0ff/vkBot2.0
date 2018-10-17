import sys
import os
import getpass
import vk_api
import time
import json
from itertools import cycle

# Get protected posts/messages
def getInfo() -> dict:
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    try:
        F = open(os.path.join(__location__, 'info.json'), "r")
    except BaseException as err:
        print("File protected.json not found " + str(err))
        exit(0)

    arr = json.load(F)

    F.close()
    return arr


def GetPickFromAniWall(vk, domain, offset):
    wall = vk.wall.get(domain=domain, offset=offset, count=1)

    if not ('photo' in wall['items'][0]['attachments'][0]):
        return None

    photos = []

    for i in wall["items"][0]['attachments']:
        owid = str(i['photo'].get('owner_id'))
        id = str(i['photo'].get('id'))
        acces = str(i['photo'].get('access_key'))

        photos.append('photo' + owid + '_' + id + '_' + acces)

    return photos

def SendMessage(vk, *data):
    if len(data) < 1:
        return 0

    if len(data) == 2:
        vk.message.send(chat_id=data[0], message=data[1])

    elif len(data) == 3:
        att = str()
        if len(data[2]) != 1:
            for i in data[2]:
                att = i + ","

            att = att[0::-1]
        else:
            att = data[2]

        vk.messages.send(chat_id=data[0], message=data[1], attachment=att)




# Get vk api object and user id
def getVkApi():
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

def main():
    FNAME = "key.txt"
    vk, token = getVkApi()

    info = getInfo()

    domain = info['domain']
    messages = info['messages']
    chat_ids = info['chat_ids']
    key = 2

    if os.path.isfile(FNAME):
        with open(FNAME, "r") as f:
            k = f.readline()
            if k != '':
                key = int(k)

    domain_cycle = cycle(domain)
    message_cycle = cycle(messages)
    while 1:
        att = GetPickFromAniWall(vk, next(domain_cycle), key)
        msg = next(message_cycle)
        if att == None:
            key += 1
            continue

        for room in chat_ids:
            SendMessage(vk, room, msg, att)
            time.sleep(0.5)

        key += 1

        with open(FNAME, "w") as f:
            f.write(str(key))

        time.sleep(30)
if __name__ == '__main__':
    main()