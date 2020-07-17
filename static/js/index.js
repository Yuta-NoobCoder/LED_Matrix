var btn_next = document.getElementById("next");
var btn_prev = document.getElementById("prev");
var btn_bright_p = document.getElementById("bright+");
var btn_bright_m = document.getElementById("bright-");

btn_next.addEventListener('click', function(){
    get("next");
});

btn_prev.addEventListener('click', function(){
    
});

btn_bright_p.addEventListener('click', function(){
    
});

btn_bright_m.addEventListener('click', function(){
    
});

function get(path){
    var request = new XMLHttpRequest();
    request.open('GET','http://192.168.1.9:8000/' + path, true);
    request.responseType = "text";
    request.onload = function(){
        console.log("OK");
    }
    request.send();
}