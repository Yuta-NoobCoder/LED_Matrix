from flask import Flask, render_template, send_file
import subprocess
import sys

app = Flask(__name__)

proc = subprocess.Popen(['sudo','python3','controll_panel.py'], encoding='utf8',stdin=subprocess.PIPE, stdout =subprocess.PIPE)

@app.route('/')
def main():                          
    return render_template("index.html")

@app.route('/next')
def next_image():
    print("next", file=proc.stdin, flush=True) 
    return ""

@app.route('/image')
def get_image():
    


if __name__ == "__main__":
    app.run()
