import os
import pyperclip
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from flask import Flask, request, redirect, url_for, session
from flask import jsonify
from flask import Blueprint
from flask import current_app as app
from flask_session import Session
import logging
from dotenv import load_dotenv

# Flaskアプリケーションのセットアップ
bp = Blueprint('bygoogledrive_up', __name__)

# ログの設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

@bp.route('/save_clipboard', methods=['POST'])
def save_clipboard():
    try:
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
        gauth.LoadCredentialsFile("credentials.json")

        if 'code' in request.args:
            gauth.Auth(request.args.get('code'))
            gauth.SaveCredentialsFile("credentials.json")
            return redirect(url_for('bygoogledrive_up.save_clipboard'))
        else:
            return jsonify({"message": "No code found in redirect"}), 500
    except Exception as e:
        logging.error(f"Error in OAuth2 callback: {str(e)}")
        return jsonify({"message": "Error in OAuth2 callback.", "error": str(e)}), 500

# FlaskアプリケーションにBlueprintを登録
app.register_blueprint(bp)
