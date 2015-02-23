// ON PAGE LOAD
$(document).ready(function() {
    // var positionCallback = null;
    // if (typeof positionFunc !== 'undefined' && $.isFunction(positionFunc)) {
    //     positionCallback = positionFunc;
    // }
    // // initialise fullPage
    // $('#fullpage').fullpage({
    //     afterRender: onload,
    //     afterResize: positionCallback,
    // });
    // setTimeout(function(){
    //     $('#fullpage').fullpage();
    // },1000);
    $(".main").onepage_scroll();
});