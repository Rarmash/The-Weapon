from dotenv import load_dotenv

from pathlib import Path
import os

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

token = os.environ["TOKEN"]
mongodb_link = os.environ["MONGODB"]
log_channel = 952519133117960192
admin_id = 390567552830406656
insider_id = 986290766848602265
admin_role_id = 646327510161686528