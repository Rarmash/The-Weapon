from dotenv import load_dotenv
from pathlib import Path
import os
import pymongo
import certifi

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

version = "2.7.0.1"

token = os.environ["TOKEN"]
mongodb_link = os.environ["MONGODB"]
fortniteapi = os.environ["FORTNITEAPI"]
xboxapi = os.environ["XBOXAPI"]
debugmode = os.environ["DEBUGMODE"]
accent_color = 0x209af8

log_channel = 952519133117960192
admin_channel = 647756597904408617
ticket_category = 1006910617833177118
poll_channel = 931963318262968412
media_channel = 966410850065874986
admin_id = 390567552830406656
mod_role_id = 646327704450236416
insider_id = 986290766848602265
admin_role_id = 646327510161686528

myclient = pymongo.MongoClient(mongodb_link, tlsCAFile=certifi.where())
Collection = myclient["Server"]["Users"]
RolesCollection = myclient["Server"]["UserRoles"]