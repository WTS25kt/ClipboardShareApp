import pyperclip
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def upload_clipboard_content():
    # Google Drive 認証
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    
    # クリップボードの内容をアップロード
    content = pyperclip.paste()
    file = drive.CreateFile({'title': 'clipboard.txt'})
    file.SetContentString(content)
    file.Upload()
    print("Clipboard content uploaded.")

if __name__ == "__main__":
    upload_clipboard_content()