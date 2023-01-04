from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

rolespath = 'roles.json'
eventspath = 'serverEvents.json'
userpath = 'users.json'
token = os.environ["TOKEN"]
mongodb_link = os.environ["MONGODB"]
fortniteapi = os.environ["FORTNITEAPI"]
debugmode = os.environ["DEBUGMODE"]
accent_color = 0x209af8

log_channel = 952519133117960192
admin_channel = 647756597904408617
ticket_category = 1006910617833177118
poll_channel = 931963318262968412
admin_id = 390567552830406656
mod_role_id = 646327704450236416
insider_id = 986290766848602265
admin_role_id = 646327510161686528