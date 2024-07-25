import pyperclip
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Google Drive 認証
gauth = GoogleAuth()

# 保存された認証情報を使用
gauth.LoadCredentialsFile("credentials.json")

if gauth.credentials is None or gauth.access_token_expired:
    gauth.LocalWebserverAuth()  # 新しい認証情報を取得
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
