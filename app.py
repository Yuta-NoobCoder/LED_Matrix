from flask import Flask, render_template, send_file
import subprocess
import sys
import base64
from io import BytesIO

app = Flask(__name__)
proc = subprocess.Popen(['sudo','python3','controll_panel.py'], encoding='utf8',stdin=subprocess.PIPE, stdout =subprocess.PIPE)

@app.route('/')
def main():
    pass
    #print("addr", file=proc.stdin, flush=True)
    #print("next", file=proc.stdin, flush=True)                          
    #return render_template("index.html")

@app.route('/signboard')
def signboard():
    return render_template("signboard.html")

@app.route('/rollsign')
def rollsign():
    proc.stdin.write("next\n")
    proc.stdin.flush()
    #print("next", file=proc.stdin, flush=True)                          
    return render_template("index.html")

@app.route('/rollsign/next')
def rollsign_next():
    proc.stdin.write("next\n")
    proc.stdin.flush()
    #print("next", file=proc.stdin, flush=True) 
    return ""

@app.route('/rollsign/prev')
def rollsign_prev():
    proc.stdin.write("prev\n")
    proc.stdin.flush()
    #print("prev", file=proc.stdin, flush=True) 
    return ""

@app.route('/rollsign/image')
def rollsign_image():
    proc.stdin.write("image\n")
    proc.stdin.flush()
    # print("image", file=proc.stdin, flush=True)
    file = str(proc.stdout.readline()).rstrip('\n')

    with open(file, 'rb') as f:
        image_str = base64.b64encode(f.read())
    return image_str 

if __name__ == "__main__":
    app.run()



