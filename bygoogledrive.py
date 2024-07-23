import pyperclip
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Google Drive 認証
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

def upload_clipboard_content():
    content = pyperclip.paste()
    file = drive.CreateFile({'title': 'clipboard.txt'})
    file.SetContentString(content)
    file.Upload()
    print("Clipboard content uploaded.")

def download_clipboard_content():
    file_list = drive.ListFile({'q': "title='clipboard.txt'"}).GetList()
    if file_list:
        file = file_list[0]
        file.GetContentFile('clipboard.txt')
        with open('clipboard.txt', 'r') as f:
            content = f.read()
        pyperclip.copy(content)
        print("Clipboard content downloaded.")

# クリップボードの内容をアップロード
upload_clipboard_content()

# クリップボードの内容をダウンロード
download_clipboard_content()