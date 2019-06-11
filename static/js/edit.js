(function () {
    console.log(" doument has loaded and readyX");

    // CSRF management for Django
    // needed for the draggable function where a POST is made
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    console.log(csrftoken)

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    $('.person').draggable({
        containment: '#myEditContainer',
        grid: [10, 10],
        start: function (element) {
            console.log("started ! ");
        },
        stop: function (element) {

            console.log("drag stopped", $(this).css("top"), $(this).css("left"), this.id);
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $.ajax({
                url: '/ajax/new_coordinates/',
                type: 'POST',
                data: {
                    'id': this.id,
                    'x_pos': $(this).css("left"),
                    'y_pos': $(this).css("top")
                },
                //type: 'POST',
                dataType: 'json',
                success: function (data) {
                    console.log("ajax success sending this data : ", data)
                }
            })

        }
    });

})();

function addPersonCsv(){
    $("#personFile").removeClass('hidden');
    $("#edgeFile").addClass('hidden');
    $("#addPerson").addClass('hidden');
    $("#addEdge").addClass('hidden');
}
function addEdgeCsv() {
    $("#edgeFile").removeClass('hidden');
    $("#personFile").addClass('hidden');
    $("#addPerson").addClass('hidden');
    $("#addEdge").addClass('hidden');
}
function addPerson() {
    $("#addPerson").removeClass('hidden');
    $("#personFile").addClass('hidden');
    $("#edgeFile").addClass('hidden');
    $("#addEdge").addClass('hidden');
}
function addEdge() {
    $("#addEdge").removeClass('hidden');
    $("#personFile").addClass('hidden');
    $("#edgeFile").addClass('hidden');
    $("#addPerson").addClass('hidden');
}


function drawEdges(data){
    localData = data
    // console.log("Surian Family selected : ", surian);

    // Remove all edges before starting building new edges
    xCount = $('.x').length
    if (xCount != 0) {
        for (var i = 0; i < xCount; i++) {
            $(".x").remove();
        }
    }

    for (i = 0; i < data.length; i++) {
        drawEdge(data[i]);
    }
    
}



function drawEdge(data) {
    // expected data structure : [ 234, [244, 245, 246, 334], 1]

    parentId = data[0];
    childrenId = data[1];
    

    if (data[2] == 1) {
        cs = '#myEditContainer';
        // return false;
    }
    if (data[2] == 2) {
        cs = '#myEditContainer';
        // if (surian == true) {
        //     return false;
        // }
    }
    if (data[2] == 3) {
        cs = '#myEditContainer';
        // if (surian == false){
        //     return false;
        // } 
    }

    // console.log("parent : ", parentId, "  children : ", childrenId)

    function getLocation(id) {
        if (id != 0) {
            // console.log(id);
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
    // console.log(" parent : ", parentTop, parentLeft);

    childTop = getLocation(childrenId[0])[1];
    childLeft = [];
    for (var i = 0; i < childrenId.length; i++) {
        childLeft[i] = getLocation(childrenId[i])[0]
    }
    // console.log("children  : ", childLeft);

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


