from dotenv import load_dotenv
from os import environ
import pymongo
import certifi
import json
from time import sleep

# Load environment variables from .env file
load_dotenv()

version = "3.0"

# Get environment variables
token = environ.get('TOKEN')
mongodb_link = environ.get('MONGODB')
fortniteapi = environ.get('FORTNITEAPI')
xboxapi = environ.get('XBOXAPI')
debugmode = environ.get('DEBUGMODE')

# Function to check and create the servers file template if it doesn't exist
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
            "elder_mod_role_id": 0,
            "junior_mod_role_id": 0,
            "insider_id": 0,
            "admin_role_id": 0,
            "trash_channels": [],
            "bannedChannels": [],
            "bannedUsers": [],
            "bannedCategories": [],
            "bannedTTSChannels": []
        }
    }
    # Create and write the servers template to servers.json
    with open('servers.json', 'w') as f:
        json.dump(servers_template, f, indent=4)
    print('Для продолжения, заполните файл servers.json.') # Print instructions for the user
    sleep(5) # Sleep for 5 seconds to give the user time to read the instructions
    exit() # Exit the program

try:
    # Try to open and load the existing servers.json file
    with open('servers.json') as f:
        servers_data = json.load(f)
except FileNotFoundError:
    # If servers.json does not exist, call the function to create it
    check_servers_file()

try:
    # Try to create a MongoDB client with the provided MongoDB link
    myclient = pymongo.MongoClient(mongodb_link)
except:
    # If an exception occurs (e.g., connection failure), try to create a MongoDB client with TLS/SSL using certifi
    myclient = pymongo.MongoClient(mongodb_link, tlsCAFile=certifi.where())