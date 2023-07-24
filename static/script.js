function popup(id){
    if (document.getElementById(id).style.display == "none"){
        document.getElementById(id).style.display = "block";
    }
    else{
        document.getElementById(id).style.display = "none";
    }
}

function cursorBlink(){
    var input = document.getElementById("url_input");
    var placeholderValue = input.placeholder;

    if (placeholderValue.endsWith("_")){
        input.placeholder = placeholderValue.substring(0, placeholderValue.length-1);
    }
    else{
        input.placeholder = placeholderValue + "_";   
    }
    setTimeout(cursorBlink, 1000);
}
// cursorBlink();



var input = "";
var demo_url = "";
var j = 0
var i = 0;
function demo(){
    var demo_urls = ["example...", "https://www.google.com", "https://www.amazon.com", "https://shaadi.com", "https://www.flipkart.com"];
    // input = document.getElementById("url_input").placeholder = "example...";
    if (j < demo_urls.length){
        demo_url = demo_urls[j];
        input = document.getElementById("url_input").placeholder = "";
        typeWriter();
        j++;
    }
    else{
        j = 0;
    }
    setTimeout(demo, 3000)
}
demo();
function typeWriter() {
    if (i < demo_url.length) {
    input = document.getElementById("url_input").placeholder += demo_url.charAt(i);
    i++;
    setTimeout(typeWriter, 100);
    }
    else{
        i = 0;
    }
}