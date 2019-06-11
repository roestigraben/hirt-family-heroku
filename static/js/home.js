


PanZoom(".content", {
    minScale: 0.2,
    maxScale: 3,
    increment: 0.01,
    liner: true
});


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


elHeight = $(".content").outerHeight();
elWidth = $(".content").outerWidth();

scale = Math.min(window.innerWidth / elWidth, (window.innerHeight) / elHeight);

x = elWidth / 2 - window.innerWidth / 2;
y = -(scale * elHeight - elHeight) / 2;

if ($("#Hirt").length){
x = x - 100;
}

var m = "matrix( " + scale + ", 0,0, " + scale + ", " + -x + ", " + -y + " )"
$(".content").css({
    "transform": m
});

//
// fit Screen
//
var fitScreen = function () {
    
    scale = Math.min(window.innerWidth / elWidth, (window.innerHeight) / elHeight);

    x = elWidth / 2 - window.innerWidth / 2;
    y = -(scale * elHeight - elHeight) / 2;

    if ($("#Hirt").length){
        x = x - 100;
    }

    var m = "matrix( " + scale + ", 0,0, " + scale + ", " + -x + ", " + -y + " )"
    $(".content").css({
        "transform": m
    });

}


//
// Zoom buttons
//
var zoomIn = function(){
    var currentScale = parseFloat($('.content').css('transform').split(',')[3]);
    var x_center = parseInt($('.content').css('transform').split(',')[4]);
    var y_center = parseInt($('.content').css('transform').split(',')[5]);

    var elHeight = $(".content").outerHeight();
    var elWidth = $(".content").outerWidth();
    var dist_mM_x = window.innerWidth / 2 - (elWidth / 2 + x_center);
    var dist_mM_y = window.innerHeight / 2 - (elHeight / 2 + y_center);
    
    var newScale = currentScale * 1.1;

    var new_x = x_center - dist_mM_x * 0.1
    var new_y = y_center - dist_mM_y * 0.1
    var m = "matrix( " + newScale + ", 0,0, " + newScale + ", " + new_x + ", " + new_y + " )"
    

    $(".content").css({
        "transform": m
    });
};
var zoomOut = function(){
    var currentScale = parseFloat($('.content').css('transform').split(',')[3]);
    var x_center = parseInt($('.content').css('transform').split(',')[4]);
    var y_center = parseInt($('.content').css('transform').split(',')[5]);

    var elHeight = $(".content").outerHeight();
    var elWidth = $(".content").outerWidth();
    var dist_mM_x = window.innerWidth / 2 - (elWidth / 2 + x_center);
    var dist_mM_y = window.innerHeight / 2 - (elHeight / 2 + y_center);

    var newScale = currentScale * 0.909;

    var new_x = x_center + dist_mM_x * 0.09
    var new_y = y_center + dist_mM_y * 0.09
    var m = "matrix( " + newScale + ", 0,0, " + newScale + ", " + new_x + ", " + new_y + " )"
   
    $(".content").css({
        "transform": m
    });
};




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
            left: -1600
        });
    }
    if (data[2] == 3) { 
        cs = '#Surian';
        $("#Surian").css({
            left: -2300
        });
    }
    
    // console.log("data    :   ", data, i); 
    // console.log("parent : ", parentId, "  children : ", childrenId)

    function getLocation(id) {
        if (id != 0) {
            x_pos = $('#' + id).css("left");
            y_pos = $('#' + id).css("top");
            // console.log("internal function log        ",id, x_pos,y_pos);
            x_pos = parseInt(x_pos.slice(0, -2));
            y_pos = parseInt(y_pos.slice(0, -2));
            return [x_pos, y_pos]
        } else {
            alert("no good");
        }
    }

    // calculate
    //console.log(" parent  : ", parentId,); 
    parent_xy = getLocation(parentId);
    //console.log(" parent coordinates : ", parentId, parent_xy[0], parent_xy[1]);

    parentTop = parent_xy[1] //getLocation(parentId)[1];
    parentLeft = parent_xy[0] //getLocation(parentId)[0];
    //console.log(" parent : ", parentId, parentTop, parentLeft);

    childTop = getLocation(childrenId[0])[1];
    childLeft = [];
    for (var i = 0; i < childrenId.length; i++) {
        childLeft[i] = getLocation(childrenId[i])[0]
    }
    //console.log("children  : ", childrenId, childTop, childLeft);

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

