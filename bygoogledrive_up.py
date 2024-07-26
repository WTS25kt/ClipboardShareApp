import pyperclip
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Google Drive 認証
gauth = GoogleAuth()
debug_messages = []

try:
    gauth.LoadCredentialsFile("credentials.json")
    debug_messages.append("Loaded credentials file.")
except Exception as e:
    debug_messages.append(f"Error loading credentials file: {e}")

if not gauth.credentials or gauth.access_token_expired:
    try:
        gauth.LocalWebserverAuth()  # ユーザー認証のためのローカルWebサーバーを起動
        gauth.SaveCredentialsFile("credentials.json")
        debug_messages.append("Performed local web server auth and saved credentials.")
    except Exception as e:
        debug_messages.append(f"Error during authentication: {e}")
else:
    try:
        gauth.Authorize()
        debug_messages.append("Authorized credentials.")
    except Exception as e:
        debug_messages.append(f"Error authorizing credentials: {e}")

try:
    drive = GoogleDrive(gauth)
    debug_messages.append("Created GoogleDrive instance.")
except Exception as e:
    debug_messages.append(f"Error creating GoogleDrive instance: {e}")

def upload_clipboard_content():
    try:
        content = pyperclip.paste()
        debug_messages.append(f"Clipboard content: {content}")
        file = drive.CreateFile({'title': 'clipboard.txt'})
        file.SetContentString(content)
        file.Upload()
        debug_messages.append("Clipboard content uploaded.")
    except Exception as e:
        debug_messages.append(f"Error uploading clipboard content: {e}")

# クリップボードの内容をアップロード
upload_clipboard_content()

for message in debug_messages:
    print(message)
