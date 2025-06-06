import os.path
import sys

from google.cloud import bigquery
from google_auth_oauthlib.flow import InstalledAppFlow

### Configuration
# Project ID
BQ_PROJECT_ID = 'myproj'
# Target table
BQ_EXTERNAL_TABLE = 'myproj.mydataset.GDriveCSVTable'
# GDrive scope. Either .../drive or .../drive.file
GDRIVE_SCOPE = 'https://www.googleapis.com/auth/drive.file'
# GDRIVE_SCOPE = 'https://www.googleapis.com/auth/drive'
###

if not os.path.exists('client_secret.json'):
    print('Provide an installed-app client_secret.json file to authenticate.')
    print('See https://github.com/googleapis/google-api-python-client/blob/main/docs/client-secrets.md')
    sys.exit(1)

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/bigquery',
            GDRIVE_SCOPE])

flow.run_local_server(port=0)

client = bigquery.Client(credentials=flow.credentials, project=BQ_PROJECT_ID)

sql = f'SELECT * FROM `{BQ_EXTERNAL_TABLE}` LIMIT 10'
query_job = client.query(sql)
rows = query_job.result()
for row in rows:
    print(row)
