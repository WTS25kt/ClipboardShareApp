import pyperclip
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def download_clipboard_content():
    # Google Drive 認証
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    
    # クリップボードの内容をダウンロード
    file_list = drive.ListFile({'q': "title='clipboard.txt'"}).GetList()
    if file_list:
        file = file_list[0]
        file.GetContentFile('clipboard.txt')
        with open('clipboard.txt', 'r') as f:
            content = f.read()
        pyperclip.copy(content)
        print("Clipboard content downloaded.")

if __name__ == "__main__":
    download_clipboard_content()