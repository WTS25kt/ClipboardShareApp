import os
import logging
from flask import Flask, render_template
from dotenv import load_dotenv

app = Flask(__name__)

# .envファイルを読み込む
load_dotenv()

# ロギングの基本設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    from bygoogledrive_up import bp as bygoogledrive_up_bp
    from bygoogledrive_dw import bp as bygoogledrive_dw_bp

    app.register_blueprint(bygoogledrive_up_bp)
    app.register_blueprint(bygoogledrive_dw_bp)

    app.run(debug=True)
