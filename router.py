from flask import Flask, render_template, send_file
import subprocess
import sys
import base64
from io import BytesIO

app = Flask(__name__)
proc = subprocess.Popen(['sudo','python3','controll_panel.py'], encoding='utf8',stdin=subprocess.PIPE, stdout =subprocess.PIPE)

@app.route('/')
def main():
    print("addr", file=proc.stdin, flush=True)
    print("next", file=proc.stdin, flush=True)                          
    return render_template("index.html")

@app.route('/next')
def next_image():
    print("next", file=proc.stdin, flush=True) 
    return ""

@app.route('/prev')
def prev_image():
    print("prev", file=proc.stdin, flush=True) 
    return ""

@app.route('/image')
def get_image():
    print("image", file=proc.stdin, flush=True)
    file = str(proc.stdout.readline()).rstrip('\n')
    with open(file, 'rb') as f:
        image_str = base64.b64encode(f.read())
    return image_str 

if __name__ == "__main__":
    app.run()



