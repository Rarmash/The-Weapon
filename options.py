from dotenv import load_dotenv
from os import environ
import pymongo
import certifi
import json
from time import sleep

load_dotenv()

version = "3.0"

token = environ.get('TOKEN')
mongodb_link = environ.get('MONGODB')
fortniteapi = environ.get('FORTNITEAPI')
xboxapi = environ.get('XBOXAPI')
debugmode = environ.get('DEBUGMODE')

def check_servers_file():
    servers_template = {
        "server_id": {
            "accent_color": "0xFFFFFF",
            "log_channel": 0,
            "admin_channel": 0,
            "ticket_category": 0,
            "suggestions_channel": 0,
            "media_channel": 0,
            "media_pins": 1,
            "admin_id": 0,
            "mod_role_id": 0,
            "insider_id": 0,
            "admin_role_id": 0,
            "trash_channels": [],
            "bannedChannels": [],
            "bannedUsers": [],
            "bannedCategories": [],
            "bannedTTSChannels": []
        }
    }
    with open('servers.json', 'w') as f:
        json.dump(servers_template, f, indent=4)
    print('Для продолжения, заполните файл servers.json.')
    sleep(5)
    exit()

try:
    with open('servers.json') as f:
        servers_data = json.load(f)
except FileNotFoundError:
    check_servers_file()

try:
    myclient = pymongo.MongoClient(mongodb_link)
except:
    myclient = pymongo.MongoClient(mongodb_link, tlsCAFile=certifi.where())