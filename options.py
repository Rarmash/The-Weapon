from dotenv import load_dotenv
from os import environ as env
import pymongo
import certifi

load_dotenv()

version = "3.0"

token = env.get('TOKEN')
mongodb_link = env.get('MONGODB')
fortniteapi = env.get('FORTNITEAPI')
xboxapi = env.get('XBOXAPI')
debugmode = env.get('DEBUGMODE')
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

if debugmode == "OFF":
    myclient = pymongo.MongoClient(mongodb_link, tlsCAFile=certifi.where())
else:
    myclient = pymongo.MongoClient(mongodb_link)
Collection = myclient["Server"]["Users"]
RolesCollection = myclient["Server"]["UserRoles"]