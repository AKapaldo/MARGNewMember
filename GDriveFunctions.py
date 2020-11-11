from __future__ import print_function
import pickle
import os.path
from emails import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/admin.directory.user']



def auth():
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
                'credentials.json', SCOPES[0])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    global service
    service = build('drive', 'v3', credentials = creds)


def getFiles(size):
    results = service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def newFolder(name, email):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder',
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    folderID = file.get('id')
    permission1 = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': email,
    }
    service.permissions().create(fileId=folderID, sendNotificationEmail=False, body=permission1).execute()
    permission2 = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': 'akapald1@gmail.com',
    }
    service.permissions().create(fileId=folderID,
                                 emailMessage='Add your certificates the the Submitted Certificates folder.',
                                 body=permission2).execute()
    print ('Folder ID: %s' % file.get('id'))


def certsFolder(name, email):
    folder_id = certs_folder
    file_metadata = {
        'name': name,
        'parents': folder_id,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    folderID = file.get('id')
    permission1 = {
        'type': 'user',
        'role': 'owner',
        'emailAddress': admin_email,
    }
    service.permissions().create(fileId=folderID, sendNotificationEmail=False, body=permission1).execute()
    permission2 = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': email,
    }
    service.permissions().create(fileId=folderID,
                                 emailMessage='Add your certificates the the Submitted Certificates folder.',
                                 body=permission2).execute()
    permission3 = {
        'type': 'group',
        'role': 'reader',
        'emailAddress': board_email,
    }
    service.permissions().create(fileId=folderID, sendNotificationEmail=False, body=permission3).execute()
    permission4 = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': training_email,
    }
    service.permissions().create(fileId=folderID, sendNotificationEmail=False, body=permission4).execute()
    print('Folder ID: %s' % file.get('id'))

def margMembers(email):
    print('Getting the first 10 users in the domain')
    results = service.users().list(customer='my_customer', maxResults=10,
                                   orderBy='email').execute()
    users = results.get('users', [])

    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            print(u'{0} ({1})'.format(user['primaryEmail'],
                                      user['name']['fullName']))
