from dotenv import load_dotenv
from os import environ as env
import pymongo
import certifi
import json

load_dotenv()

version = "3.0"

token = env.get('TOKEN')
mongodb_link = env.get('MONGODB')
fortniteapi = env.get('FORTNITEAPI')
xboxapi = env.get('XBOXAPI')
debugmode = env.get('DEBUGMODE')

with open('servers.json') as f:
    servers_data = json.load(f)

try:
    myclient = pymongo.MongoClient(mongodb_link)
except:
    myclient = pymongo.MongoClient(mongodb_link, tlsCAFile=certifi.where())