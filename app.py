import os
import subprocess
import logging
from flask import Flask, jsonify, render_template, redirect, url_for, request
from dotenv import load_dotenv

app = Flask(__name__)

# .envファイルを読み込む
load_dotenv()

# ロギングの基本設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

# 環境変数からファイルを書き出す
client_secrets_content = os.getenv('CLIENT_SECRETS_JSON')
credentials_content = os.getenv('CREDENTIALS_JSON')

if client_secrets_content:
    with open('client_secrets.json', 'w') as f:
        f.write(client_secrets_content)

if credentials_content:
    with open('credentials.json', 'w') as f:
        f.write(credentials_content)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    from bygoogledrive_up import bp as bygoogledrive_up_bp
    from bygoogledrive_dw import bp as bygoogledrive_dw_bp

    app.register_blueprint(bygoogledrive_up_bp)
    app.register_blueprint(bygoogledrive_dw_bp)

    app.run(debug=True)
