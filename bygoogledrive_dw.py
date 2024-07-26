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

def download_clipboard_content():
    try:
        file_list = drive.ListFile({'q': "title='clipboard.txt'"}).GetList()
        if file_list:
            file = file_list[0]
            file.GetContentFile('clipboard.txt')
            with open('clipboard.txt', 'r') as f:
                content = f.read()
            pyperclip.copy(content)
            debug_messages.append(f"Clipboard content: {content}")
            debug_messages.append("Clipboard content downloaded.")
        else:
            debug_messages.append("No file named 'clipboard.txt' found.")
    except Exception as e:
        debug_messages.append(f"Error downloading clipboard content: {e}")

# クリップボードの内容をダウンロード
download_clipboard_content()

for message in debug_messages:
    print(message)
