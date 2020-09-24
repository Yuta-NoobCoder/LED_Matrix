var btn_next = document.getElementById("btn_next");
var btn_prev = document.getElementById("btn_prev");
var chk_auto_switch = document.getElementById("chk_auto_switch"); //自動切り替え
var txt_interval = document.getElementById("txt_interval"); //間隔
var select_interval = document.getElementById("select_interval"); //単位
var lbl_interval = document.getElementById("lbl_interval");
var current_image = document.getElementById("led");

var timer;
var interval;
var response;

//読み込み時の自動切り替え処理
window.onload = function () {
    //チェック状態を反映
    chk_auto_switch.checked = localStorage.checked;
    txt_interval.value = localStorage.interval;
    if (chk_auto_switch.checked == true) {
        //切り替え間隔
        interval = txt_interval.value;
        if (select_interval.value == "min") interval *= 60;
        //自動切り替えを有効化
        ajax("/rollsign/action?type=enable_auto&interval=" + interval);
        //タイマーを起動
        timer = setInterval(function () {
            ajax("/rollsign/action?type=image");
        }, interval * 1000);
    }
}

btn_next.addEventListener('click', function () {
    ajax("/rollsign/action?type=next");
});

btn_prev.addEventListener('click', function () {
    ajax("/rollsign/action?type=prev");
});

chk_auto_switch.addEventListener('change', function () {
    if (chk_auto_switch.checked == true) {
        //切り替え有無・間隔を保存
        localStorage.checked = true;
        localStorage.interval = txt_interval.value;
        //要素を有効化
        txt_interval.disabled = false;
        select_interval.disabled = false;
        lbl_interval.style.opacity = 1.0;
        //切り替え間隔
        interval = txt_interval.value;
        if (select_interval.value == "min") interval *= 60;
        //自動切り替えを有効化
        ajax("/rollsign/action?type=enable_auto&interval=" + interval);
        //タイマーを起動
        timer = setInterval(function () {
            ajax("/rollsign/action?type=image");
        }, interval * 1000);
    }
    else {
        //チェック状態を保存
        localStorage.checked = false;
        //要素を無効化
        txt_interval.disabled = true;
        select_interval.disabled = true;
        lbl_interval.style.opacity = 0.5;
        //タイマーを停止
        ajax("/rollsign/action?type=disable_auto");
        clearInterval(timer);
    }
});


function ajax(url) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = function () {
        //next,prev,imageコマンドでのみ画像を変更
        if (request.responseText.indexOf("data:image") != -1) {
            current_image.src = request.responseText;
        }
    }
    request.send();
}
