var btn_next = document.getElementById("next");
var btn_prev = document.getElementById("prev");
var current_image = document.getElementById("led");

btn_next.addEventListener('click', function(){
    xhr("/rollsign/action?type=next");
});

btn_prev.addEventListener('click', function(){
    xhr("/rollsign/action?type=prev");
});

window.onload = function () {
    //開始時の画像を取得
    xhr("/rollsign/action?type=image");
}

function xhr(path){
    var request = new XMLHttpRequest();
    request.open('GET', path, true);
    request.onload = function(){
        console.log(request.responseText);
        current_image.src = request.responseText;
    }
    request.send();
}
