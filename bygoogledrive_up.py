import os
import pyperclip
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# Google Drive 認証
gauth = GoogleAuth()

# 環境変数から認証情報を読み込む
client_secrets_content = os.getenv('CLIENT_SECRETS_JSON')
credentials_content = os.getenv('CREDENTIALS_JSON')

if client_secrets_content:
    with open('client_secrets.json', 'w') as f:
        f.write(client_secrets_content)

if credentials_content:
    with open('credentials.json', 'w') as f:
        f.write(credentials_content)

# 保存された認証情報を使用
gauth.LoadCredentialsFile("credentials.json")

if gauth.credentials is None or gauth.access_token_expired:
    gauth.CommandLineAuth()  # コマンドライン認証フローを使用
    gauth.SaveCredentialsFile("credentials.json")  # 認証情報を保存

drive = GoogleDrive(gauth)

def upload_clipboard_content():
    content = pyperclip.paste()
    file = drive.CreateFile({'title': 'clipboard.txt'})
    file.SetContentString(content)
    file.Upload()
    print("Clipboard content uploaded.")

# クリップボードの内容をアップロード
upload_clipboard_content()