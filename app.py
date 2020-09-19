from flask import Flask, render_template, send_file, request
import subprocess
import sys
import base64

app = Flask(__name__)

proc = subprocess.Popen(
    ['sudo', 'python3', 'controll_panel.py'],
    encoding='utf8',
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE
)

@app.route('/')
def main():
    pass

@app.route('/signboard')
def signboard():
    return render_template("signboard.html")


@app.route('/rollsign')
def rollsign():
    #最初の画像を取得
    proc.stdin.write("image\n")
    proc.stdin.flush()
    image_url = proc.stdout.readline().rstrip("\n")
    return render_template("index.html", src=image_url)


@app.route('/rollsign/action')
def controll_rollsign():

    action_type = request.args.get("type")

    if action_type == "next":
        proc.stdin.write("next\n")
    elif action_type == "prev":
        proc.stdin.write("prev\n")
    elif action_type == "image":
        proc.stdin.write("image\n")

    proc.stdin.flush()

    return proc.stdout.readline().rstrip("\n")

