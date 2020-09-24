from flask import Flask, render_template, request, make_response, jsonify
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
    return render_template("index.html")


@app.route('/signboard')
def signboard():
    return render_template("signboard.html")


@app.route('/rollsign')
def rollsign():
    # 最初の画像を取得
    proc.stdin.write("image\n")
    proc.stdin.flush()
    image_url = proc.stdout.readline().rstrip("\n")
    return render_template("rollsign.html", src=image_url)


@app.route('/rollsign/action')
def controll_rollsign():

    action_type = request.args.get("type")

    if action_type == "next" or action_type == "prev" or action_type == "image":

        if action_type == "next":
            proc.stdin.write("next\n")
        elif action_type == "prev":
            proc.stdin.write("prev\n")
        elif action_type == "image":
            proc.stdin.write("image\n")

        proc.stdin.flush()
        return proc.stdout.readline().rstrip("\n")

    elif action_type == "enable_auto":
        interval = request.args.get("interval")
        if interval:
            proc.stdin.write("enable_auto," + interval + "\n")
            proc.stdin.flush()
            # コンテンツなし
            response = make_response(jsonify(None), 204)
        return response

    elif action_type == "disable_auto":
        proc.stdin.write("disable_auto\n")
        proc.stdin.flush()
        response = make_response(jsonify(None), 204)
        return response
