from __future__ import print_function

import base64
from email.mime.text import MIMEText
import google.auth

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.r']


# def gmail_create_draft(creds):
#     """Create and insert a draft email.
#        Print the returned draft's message and id.
#        Returns: Draft object, including draft id and message meta data.
#
#       Load pre-authorized user credentials from the environment.
#       TODO(developer) - See https://developers.google.com/identity
#       for guides on implementing OAuth2 for the application.
#     """
#     # creds, _ = google.auth.default()
#
#     try:
#         # create gmail api client
#         service = build('gmail', 'v1', credentials=creds)
#
#         message = MIMEText('This is automated draft mail')
#         message['To'] = 'gibbs.airflow@gmail.com'
#         message['From'] = 'gibbs.airflow@gmail.com'
#         message['Subject'] = 'Automated draft'
#         encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
#
#         create_message = {
#             'message': {
#                 'raw': encoded_message
#             }
#         }
#         # pylint: disable=E1101
#         draft = service.users().drafts().create(userId="me",
#                                                 body=create_message).execute()
#
#         print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
#
#     except HttpError as error:
#         print(F'An error occurred: {error}')
#         draft = None
#
#     return draft


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # gmail_create_draft(creds)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # gmail_create_draft(creds)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText('This is automated draft mail')
        message['To'] = 'gibbs.airflow@gmail.com'
        message['From'] = 'gibbs.airflow@gmail.com'
        message['Subject'] = 'Automated draft'
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'message': {
                'raw': encoded_message
            }
        }
        # pylint: disable=E1101
        draft = service.users().drafts().create(userId="me",
                                                body=create_message).execute()

        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None

    return draft

    # try:
    #     # Call the Gmail API
    #     service = build('gmail', 'v1', credentials=creds)
    #     results = service.users().labels().list(userId='me').execute()
    #     labels = results.get('labels', [])
    #
    #     if not labels:
    #         print('No labels found.')
    #         return
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])
    #
    # except HttpError as error:
    #     # TODO(developer) - Handle errors from gmail API.
    #     print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
