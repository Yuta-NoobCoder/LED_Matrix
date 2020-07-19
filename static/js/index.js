var btn_next = document.getElementById("next");
var btn_prev = document.getElementById("prev");
var btn_bright_p = document.getElementById("bright+");
var btn_bright_m = document.getElementById("bright-");
var current_image = document.getElementById("led");

btn_next.addEventListener('click', function(){
    get("next");
    get("image"); 
});

btn_prev.addEventListener('click', function(){
    get("prev");
    get("image"); 
});

btn_bright_p.addEventListener('click', function(){
    
});

btn_bright_m.addEventListener('click', function(){
    
});

window.onload = function(){
    get("image");
}

function get(path){
    var request = new XMLHttpRequest();
    request.open('GET','http://192.168.1.9:8000/' + path, true);
    request.onload = function(){
        if(path == "image"){
            current_image.src =  "data:image/png;base64," + request.responseText;
        }
    }
    request.send();
}
