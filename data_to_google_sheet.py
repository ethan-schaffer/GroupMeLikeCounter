# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]

# This code has been modified based on example code found at https://developers.google.com/sheets/api/quickstart/python
# It is not intended for commercial use

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
f = open("sheet_id.txt", "r")
SPREADSHEET_ID = f.read()
RANGE_NAME = 'Info!A1:D'


creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

def save_json(obj, name):
    with open('obj/'+ name + '.json', 'w') as f:
        f.write(json.dumps(obj))

def load_json(name):
    with open('obj/'+ name + '.json', 'r') as f:
        return json.loads(f.read())

def get_name_from_member_id(id, id_to_member, stats):
    if id in id_to_member:
        return id_to_member[id]
    return f"Removed Member: {stats}"

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def load_rest(name):
    with open('obj/' + name + '.txt', 'rb') as f:
        file_text = f.readlines()
        json_dt = json.loads(file_text[1])
        return file_text[0].decode("utf-8")[:-1], json_dt, file_text[2], file_text[3]

people = load_json("people_data")
for person in people:
    people[person] = (people[person][0], people[person][1], set(people[person][2]))

group_name, id_to_member, total_messages, last_message_id = load_rest("additional_data")

lst = []
for person in people:
    stats = people[person]
    name = get_name_from_member_id(person, id_to_member, stats[2])
    if "Removed Member" not in name:
        lst.append([round(stats[0]/stats[1],2), stats[0], stats[1], name])

# lst.sort(key=lambda x: x[1], reverse=True)
lst.sort(reverse=True)
dt = [["Likes Per Message", "Likes Total", "Total Messages", "User"]]
dt.extend(lst)

my_data = {'values': dt}

print("Sending data:")
print(dt)

value = service.spreadsheets().values()
process = value.update(spreadsheetId=SPREADSHEET_ID,
                       range='Info!A2:D', valueInputOption='RAW', body=my_data)
process.execute()

lst.sort(key=lambda x: x[1], reverse=True)
lst = map(lambda x: [x[1], x[2], x[0], x[3]], lst)
dt = [["Likes Total", "Total Messages", "Likes Per Message", "User"]]
dt.extend(lst)

my_data = {'values': dt}

print("Sending data:")
print(dt)

value = service.spreadsheets().values()
process = value.update(spreadsheetId=SPREADSHEET_ID,
                       range='Info!F2:I', valueInputOption='RAW', body=my_data)
process.execute()

print("Updated!")
