import os
import pyperclip
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from flask import Flask, request, redirect, url_for, session, jsonify, Blueprint
import logging
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# Flaskアプリケーションのセットアップ
bp = Blueprint('bygoogledrive_up', __name__)

# ログの設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

@bp.route('/save_clipboard', methods=['POST'])
def save_clipboard():
    try:
        # Google Drive 認証
        gauth = GoogleAuth()

        # クライアントシークレットを環境変数から取得
        client_secrets_content = os.getenv('CLIENT_SECRETS_JSON')
        with open('client_secrets.json', 'w') as f:
            f.write(client_secrets_content)

        gauth.LoadClientConfigFile("client_secrets.json")

        if gauth.credentials is None or gauth.access_token_expired:
            auth_url = gauth.GetAuthUrl()
            return redirect(auth_url)
        else:
            gauth.Refresh()

        drive = GoogleDrive(gauth)

        # クリップボードの内容をアップロード
        content = pyperclip.paste()
        file = drive.CreateFile({'title': 'clipboard.txt'})
        file.SetContentString(content)
        file.Upload()

        return jsonify({"message": "Clipboard content uploaded."})
    except Exception as e:
        logging.error(f"Error uploading clipboard content: {str(e)}")
        return jsonify({"message": "Error uploading clipboard content.", "error": str(e)}), 500

@bp.route('/oauth2callback')
def oauth2callback():
    try:
        gauth = GoogleAuth()

        gauth.LoadClientConfigFile("client_secrets.json")

        if 'code' in request.args:
            gauth.Auth(request.args.get('code'))
            return redirect(url_for('bygoogledrive_up.save_clipboard'))
        else:
            return jsonify({"message": "No code found in redirect"}), 500
    except Exception as e:
        logging.error(f"Error in OAuth2 callback: {str(e)}")
        return jsonify({"message": "Error in OAuth2 callback.", "error": str(e)}), 500

# FlaskアプリケーションにBlueprintを登録
app.register_blueprint(bp)
