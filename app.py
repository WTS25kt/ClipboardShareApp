import subprocess
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_clipboard', methods=['POST'])
def save_clipboard():
    try:
        result = subprocess.run(['python3', 'bygoogledrive_up.py'], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "Clipboard content uploaded."})
        else:
            return jsonify({"message": "Error uploading clipboard content.", "error": result.stderr}), 500
    except Exception as e:
        return jsonify({"message": "Error uploading clipboard content.", "error": str(e)}), 500

@app.route('/load_clipboard', methods=['GET'])
def load_clipboard():
    try:
        result = subprocess.run(['python3', 'bygoogledrive_dw.py'], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "Clipboard content downloaded."})
        else:
            return jsonify({"message": "Error downloading clipboard content.", "error": result.stderr}), 500
    except Exception as e:
        return jsonify({"message": "Error downloading clipboard content.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

#07251645 うまくいかなかったので、07251015時点まで戻したが、認証がうまくいかなくなってしまったので、明日また実行しうまくいかなければ1から作り直す