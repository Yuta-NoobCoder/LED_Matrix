from flask import Flask, render_template, request, make_response, jsonify
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from apscheduler.schedulers.background import BackgroundScheduler
from rollsign import Rollsign


# マトリクスの初期化
options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'
options.rows = 32
options.cols = 128
options.brightness = 50
options.gpio_slowdown = 4
options.pwm_lsb_nanoseconds = 100
matrix = RGBMatrix(options=options)

rollsign = Rollsign(matrix)
rollsign.set_images_dir("images")

scheduler = BackgroundScheduler()
scheduler.add_job(rollsign.next_image, "interval", seconds=30, id="auto_switch")
scheduler.start(paused=True)

app = Flask(__name__)

@app.route('/')
def root():
    # 最初の画像を表示・取得
    rollsign.show()
    return render_template("rollsign.html", src=rollsign.get_base64_image())

@app.route('/rollsign/action')
def controll_rollsign():

    action_type = request.args.get("type")

    if action_type == "next" or action_type == "prev" or action_type == "image":

        if action_type == "next":
            rollsign.next_image()
        elif action_type == "prev":
            rollsign.prev_image()
            
        return rollsign.get_base64_image()

    elif action_type == "enable_auto_switch":

        interval = request.args.get("interval")
        scheduler.reschedule_job(
            "auto_switch", trigger="interval", seconds=int(interval))
        scheduler.resume()
        # コンテンツなし
        response = make_response(jsonify(None), 204)
        return response

    elif action_type == "disable_auto_switch":
        
        scheduler.pause()
        response = make_response(jsonify(None), 204)
        return response
