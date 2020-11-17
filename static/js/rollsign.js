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

window.onload = function () 
{
    //初回アクセス時の要素の状態を保存
    if (!localStorage.interval || !localStorage.checked)
    {
        localStorage.interval = "30";
        localStorage.checked = "0";
    }
    //間隔を反映(分単位の場合は60倍)
    txt_interval.value = localStorage.interval;
    if (select_interval.value == "min") interval *= 60;
    //自動切り替えを有効化
    if (parseInt(localStorage.checked)) 
    {
        //チェック状態を反映{
        chk_auto_switch.checked = true;
        ajax("/rollsign/action?type=enable_auto&interval=" + interval)
        current_image.style.opacity = 0.5;
    }
}

btn_next.addEventListener('click', function () 
{
    ajax("/rollsign/action?type=next");
});

btn_prev.addEventListener('click', function () 
{
    ajax("/rollsign/action?type=prev");
});

chk_auto_switch.addEventListener('change', function () 
{
    //切り替え間隔を保存
    localStorage.interval = txt_interval.value;
    console.log(localStorage.checked);

    if (chk_auto_switch.checked == true) {
        localStorage.checked = "1";
        //要素を有効化
        txt_interval.disabled = false;
        select_interval.disabled = false;
        lbl_interval.style.opacity = 1.0;
        //切り替え間隔
        interval = txt_interval.value;
        if (select_interval.value == "min") interval *= 60;
        //自動切り替えを有効化
        ajax("/rollsign/action?type=enable_auto_switch&interval=" + interval);
        //自動切り替え中はプレビュー未使用
        current_image.style.opacity = 0.5;
    }
    else 
    {
        //チェック状態を保存
        localStorage.checked = "0";
        //要素を無効化
        txt_interval.disabled = true;
        select_interval.disabled = true;
        lbl_interval.style.opacity = 0.5;
        //プレビューを再開
        current_image.style.opacity = 1.0;
        ajax("/rollsign/action?type=disable_auto_switch");
        ajax("/rollsign/action?type=image");
    }
});


function ajax(url) 
{
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = function () 
    {
        //next,prev,imageコマンドでのみ画像を変更
        if (request.responseText.indexOf("data:image") != -1) 
        {
            current_image.src = request.responseText;
        }
    }
    request.send();
}
