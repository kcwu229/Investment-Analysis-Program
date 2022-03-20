function swapSlide(){
    var s1 = document.getElementById("slide1");
    var s2 = document.getElementById("slide2");
    var logo = document.getElementById("logoFooter");
    var subscribe = document.getElementById("subscribe");
    var bgColor = document.getElementById("bg-color");
    if (s1.style.display == 'block') {
        s1.style.display = 'none';
        s2.style.display = 'block';
        logo.style.color = 'rgba(0, 195, 255, 0.815)';
        subscribe.style.backgroundColor = 'rgba(0, 195, 255, 0.815)';
        bgColor.style.backgroundColor = 'rgba(0, 195, 255, 0.815)';
    }
    else {
        s2.style.display = 'none';
        s1.style.display = 'block';
        logo.style.color = '#de736fd3';
        subscribe.style.backgroundColor = '#de736fd3';
        bgColor.style.backgroundColor = '#de736fd3';
    }
    
}

function autoSwap() {
    // Change Image in every 10 seconds
    window.setInterval(swapSlide, 10000);
}
