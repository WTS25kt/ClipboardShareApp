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

# クリップボードの内容をアップロード
upload_clipboard_content()

#07251645 うまくいかなかったので、07251015時点まで戻したが、認証がうまくいかなくなってしまったので、明日また実行しうまくいかなければ1から作り直す
