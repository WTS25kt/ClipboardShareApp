import tkinter as tk
import subprocess

def run_upload_script():
    subprocess.run(["python", "bygoogledrive_up.py"])

def run_download_script():
    subprocess.run(["python", "bygoogledrive_dw.py"])

# ウィンドウの作成
root = tk.Tk()
root.title("Clipboard Share App")
root.geometry("300x200")

# アップロードボタン
upload_button = tk.Button(root, text="Upload Clipboard", command=run_upload_script)
upload_button.pack(pady=10)

# ダウンロードボタン
download_button = tk.Button(root, text="Download Clipboard", command=run_download_script)
download_button.pack(pady=10)

# メインループの開始
root.mainloop()