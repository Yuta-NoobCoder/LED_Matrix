var btn_next = document.getElementById("btn_next");
var btn_prev = document.getElementById("btn_prev");
var chk_auto_switch = document.getElementById("chk_auto_switch"); //自動切り替え
var txt_interval = document.getElementById("txt_interval"); //間隔
var select_interval = document.getElementById("select_interval"); //単位
var lbl_interval = document.getElementById("lbl_interval");
var current_image = document.getElementById("led");

window.onbeforeunload = function () {
    xhr("/rollsign/action?type=leave")
}


btn_next.addEventListener('click', function () {
    xhr("/rollsign/action?type=next");
});

btn_prev.addEventListener('click', function () {
    xhr("/rollsign/action?type=prev");
});

var timer;
chk_auto_switch.addEventListener('change', function () {
    if (chk_auto_switch.checked == true) {
        txt_interval.disabled = false;
        select_interval.disabled = false;
        lbl_interval.style.opacity = 1.0;
        //タイマーをスタート
        var interval = txt_interval.value * 1000; //秒換算
        if (select_interval.value = "min") interval *= 60;
        timer = setInterval(function () {
            xhr("/rollsign/action?type=next");
        }, interval);
    }
    else {
        txt_interval.disabled = true;
        select_interval.disabled = true;
        lbl_interval.style.opacity = 0.5;
        //タイマーを停止
        clearInterval(timer);
    }
});

function xhr(path) {
    var request = new XMLHttpRequest();
    request.open('GET', path, true);
    request.onload = function () {
        current_image.src = request.responseText;
    }
    request.send();
}
