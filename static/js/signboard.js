var btn = document.getElementById("button");
var text = document.getElementById("text");

var row = document.getElementById("row1");

var radio = document.getElementById("radio");

btn.value = "色変更";

btn.addEventListener('click', function(){
    var start = text.selectionStart;
    var end = text.selectionEnd;
    var radioNodeList = radio.color;
    console.log(radioNodeList);
    if(radioNodeList.value === "red")
    {
        row1.value = row1.value + "<span style = \"color:#ff0000\">"
        console.log(radioNodeList, row1.value);
    }
})


/*
function get(path){
    var request = new XMLHttpRequest();
    request.open('GET', path, true);
    request.onload = function(){
        if(path == "/rollsign/image"){
            console.log(request.responseText);
            current_image.src =  "data:image/png;base64," + request.responseText;
        }
    }
    request.send();
}
*/