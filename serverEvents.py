#time is in GMT +0
import json

with open("serverEvents.json", "r") as file:
    data = json.load(file)

serverEventsDates = []
serverEventsTitles = []
serverEventsDescriptions = []
serverEventsIcons = []

for i in data:
    serverEventsTitles.append(data[i][0][u'title'])
    serverEventsDescriptions.append(data[i][0][u'description'])
    serverEventsIcons.append(data[i][0][u'icon'])
    serverEventsDates.append(data[i][0][u'date'])