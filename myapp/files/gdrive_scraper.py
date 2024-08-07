import os
import csv
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Replace these values with your actual credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
REFRESH_TOKEN = ''

def authenticate_gdrive():
    """Authenticates and returns the Google Drive service using refresh token."""
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )

    service = build('drive', 'v3', credentials=creds)
    return service

def extract_file_id(file_link):
    """Extracts the file ID from a Google Drive file link."""
    match = re.search(r'/d/([^/]+)', file_link)
    return match.group(1) if match else 'No ID available'

def extract_episode_number(file_name):
    """Extracts episode number from file name."""
    match = re.search(r'OP - (\d+)', file_name)
    return match.group(1) if match else 'No number available'

def list_files(service, folder_id):
    """Lists files in a specific folder and returns their names, file IDs, links, episode numbers, and folder ID."""
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=1000,
        fields="nextPageToken, files(id, name, webViewLink)"
    ).execute()

    items = results.get('files', [])
    file_data = [
        (
            item['name'].replace('.mkv', '').replace('One Piece', 'OP'),
            extract_file_id(item.get('webViewLink', 'No link available')),
            extract_episode_number(item['name'].replace('.mkv', '').replace('One Piece', 'OP'))  # Extract episode number
        )
        for item in items
    ]

    return file_data

def save_to_csv(file_data, filename=r'gdrive_files_ids.csv'):
    """Saves file data to a CSV file, appending data and writing headers only if the file is new or headers are missing."""
    file_exists = os.path.isfile(filename)

    # Check if the file exists and if it already has headers
    if file_exists:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            # Read the first row to check for headers
            headers = next(reader, None)
            headers_exist = headers == ['file_name', 'file_id', 'episode_number']
    else:
        headers_exist = False

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the header only if it does not exist
        if not headers_exist:
            writer.writerow(['file_name', 'file_id', 'episode_number'])
        writer.writerows(file_data)

def main():
    folders = [

    ]

    service = authenticate_gdrive()

    for folder_id in folders:
        file_data = list_files(service, folder_id)
        save_to_csv(file_data)

if __name__ == '__main__':
    main()
