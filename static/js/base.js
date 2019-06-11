(function() {
    console.log(" doument has loaded and ready")

    PanZoom(".panzoom", {
        minScale: 0.2,
        maxScale: 3,
        increment: 0.01,
        liner: true
    });

    // document.querySelector("#myContainer").style.transform = 'matrix(0.5, 0, 0, 0.5, -1000, -400)';   
    // scale = 0.5;
    // $("#myContainer").css({ transform: "translate(0%, -20%) " + "scale(" + scale + ")" });

})();

$(".person").hover(
    function () {
        $(this).addClass("animated");
    },
    function () {
        $(this).removeClass("animated");
    }
);

//
//  initial scaling of the div (id = myContainer) to fill the browser window 
//
var $el = $("#myContainer");
var elHeight = $el.outerHeight();
var elWidth = $el.outerWidth();
// 
// console.log($(".navbar-header").outerHeight());
// console.log("myContainer outer width and height : ", elWidth, elHeight);
// console.log("Browser outer width and height : ", window.outerWidth, window.outerHeight);
// console.log("Browser inner width and height : ", window.innerWidth, window.innerHeight);
// console.log("ratio width - ratio height : ", window.innerWidth / elWidth, window.innerHeight / elHeight)


scale = Math.min(window.innerWidth / elWidth, (window.innerHeight - 60) / elHeight);
//$el.css({ transform: "translate(-50%, -30%) " + "scale(" + scale + ")" });
$el.css({ "transform": "scale(" + scale + ")" });
// console.log("initial scale = ", scale)

//
// adjust div to browser window changes
//
var onresize = function (e) {
    //note i need to pass the event as an argument to the function
    width = e.target.innerWidth;
    height = e.target.innerHeight;
    //console.log(width, height);

    scale = Math.min(width / elWidth, (height - 60) / elHeight);
    //console.log(scale);

    //$el.css({ transform: "translate(-50%, -30%) " + "scale(" + scale + ")" });
    $el.css({ "transform": "scale(" + scale + ")" });


}
window.addEventListener("resize", onresize);

//
// Zoom buttons
//
var zoomIn = function(){
    scale = scale * 1.1;
    $el.css({
        "transform": "scale(" + scale + ")"
    });
}
var zoomOut = function(){
    scale = scale * 0.9;
    $el.css({
        "transform": "scale(" + scale + ")"
    });
}




function drawEdges(data, i) {
    // expected data structure : [ 234, [244, 245, 246, 334]]
    parentId = data[0];
    childrenId = data[1];
    /* 
    if (i>=family_id){
        return
    }
     */
 
    if (data[2] == 1) { 
        cs = '#Hirt';
    }
    if (data[2] == 2) {
        cs = '#Schwab';
        $("#Schwab").css({
            left: -1400
        });
    }
    if (data[2] == 3) { 
        cs = '#Surian';
        $("#Surian").css({
            left: -1500
        });
    }
    
        
    //console.log("parent : ", parentId, "  children : ", childrenId)

    function getLocation(id) {
        if (id != 0) {
            x_pos = $('#' + id).css("left");
            y_pos = $('#' + id).css("top");
            x_pos = parseInt(x_pos.slice(0, -2));
            y_pos = parseInt(y_pos.slice(0, -2));
            return [x_pos, y_pos]
        } else {
            alert("no good");
        }
    }

    // calculate 
    parentTop = getLocation(parentId)[1];
    parentLeft = getLocation(parentId)[0];
    //console.log(" parent : ", parentTop, parentLeft);

    childTop = getLocation(childrenId[0])[1];
    childLeft = [];
    for (var i = 0; i < childrenId.length; i++) {
        childLeft[i] = getLocation(childrenId[i])[0]
    }
    //console.log("children  : ", childLeft);

    childrenHeight = 40;
    horizontalTop = childTop - childrenHeight;
    parentHeight = childTop - parentTop - childrenHeight

    // define mid point of person div
    w = $('.person').css("width")
    personWidthBias = parseInt(w.slice(0, -2) / 2)
    //console.log(personWidthBias);

    // determine which of the children are the most left and most right
    mostLeft = childLeft[0];
    mostRight = childLeft[0];
    for (var i = 0; i < childLeft.length; i++) {
        if (mostLeft > childLeft[i]) {
            mostLeft = childLeft[i];
        }
        if (mostRight < childLeft[i]) {
            mostRight = childLeft[i];
        }
    }
    // console.log("most left and most right : ", mostLeft, mostRight)


    horizontalWidth = mostRight - mostLeft;
    mostLeft = mostLeft + personWidthBias;
    //console.log(mostLeft, horizontalWidth);
    
    // create divs for all legs of the parent child connections
    for (var i = 0; i < childrenId.length; i++) {
        //console.log("i");
        $(cs).append('<div class="x borderLeft" style="top:' + horizontalTop.toString() + 'px;left:' + (childLeft[i] + personWidthBias).toString() + 'px;height:' + childrenHeight.toString() + 'px;"></div>')
        $(cs).append('<div class="x borderLeft" style="top:' + horizontalTop.toString() + 'px;left:' + (childLeft[i] + personWidthBias).toString() + 'px;height:' + childrenHeight.toString() + 'px;"></div>')
        $(cs).append('<div class="x borderLeft" style="top:' + horizontalTop.toString() + 'px;left:' + (childLeft[i] + personWidthBias).toString() + 'px;height:' + childrenHeight.toString() + 'px;"></div>')
    }

    // add the edges defined by divs
    $(cs).append('<div class="x borderLeft" style="top:' + parentTop.toString() + 'px;left:' + parentLeft.toString() + 'px;height:' + parentHeight.toString() + 'px;"></div>')
    $(cs).append('<div class="x borderTop" style="top:' + horizontalTop.toString() + 'px;left:' + mostLeft.toString() + 'px;width:' + horizontalWidth.toString() + 'px;"></div>')

    if (mostLeft > parentLeft) {
        newWidth = mostLeft - parentLeft;
        $(cs).append('<div class="x borderTop" style="top:' + horizontalTop.toString() + 'px;left:' + parentLeft.toString() + 'px;width:' + newWidth.toString() + 'px;"></div>')
    }
    if (mostRight < parentLeft) {
        newWidth = parentLeft - mostRight - personWidthBias;
        $(cs).append('<div class="x borderTop" style="top:' + horizontalTop.toString() + 'px;left:' + (mostRight + personWidthBias).toString() + 'px;width:' + newWidth.toString() + 'px;"></div>')
    }


}