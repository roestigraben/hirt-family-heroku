// Inital method to call to apply PanZoom to elements given a selector
function PanZoom(selector, opts) {
    let panZoomEles = []
    opts = opts || {};
    let minScale = (opts.minScale ? opts.minScale : 0.1);
    let maxScale = (opts.maxScale ? opts.maxScale : 5);
    let increment = (opts.increment ? opts.increment  : 0.05);
    let liner = (opts.liner ? opts.liner  : false);
    //console.log("the opts object is : ", opts);
    //console.log("default values -> minScale : ", minScale, " maxScale : ", maxScale, " etc.etc. ");
    //console.log("selector is : ", selector)
    document.querySelectorAll(selector).forEach(function(ele){
        panZoomEles.push(new AttachPanZoom(ele, minScale , maxScale, increment, liner));
        //console.log("panZoomElements are : ", panZoomEles[0]);
    });
    if(panZoomEles.length == 1)
        return panZoomEles[0];
    return panZoomEles;
}

// Appy PanZoom functionality to a given element, allow user defined zoom min and inc per scroll
function AttachPanZoom(ele, minScale, maxScale, increment, liner) {
  this.increment = increment;
    //console.log("increment as passed into class instance", this.increment);
    //console.log("ele :         ", ele);
  this.minScale = minScale;
  this.maxScale = maxScale;
  this.liner = liner;
  this.panning = false;
  this.oldX = this.oldY = 0;
  let self = this;
  ele.style.transform = "matrix(1, 0, 0, 1, 0, 0)";
  
  // Gets the current Scale, along with transX and transY
  this.getTransformMatrix = function() {
    let trans = ele.style.transform;
    let start = trans.indexOf("(") + 1;
    let end = trans.indexOf(")");
    let matrix = trans.slice(start, end).split(",");
    return { 
      "scale": +matrix[0], 
      "transX": +matrix[4], 
      "transY": +matrix[5] 
    }
  }

  // Given the scale, translateX and translateY apply to CSS transform
  this.setTransformMatrix = function(o) {
    ele.style.transform = 'matrix('+o.scale+', 0, 0, '+o.scale+', '+o.transX+', '+o.transY+')';
    //console.log('the translate values are :     ', 'matrix(' + o.scale + ', 0, 0, ' + o.scale + ', ' + o.transX + ', ' + o.transY + ')')
  }

  this.applyTranslate = function(dx, dy){
    let newTrans = this.getTransformMatrix();
    newTrans.transX += dx;
    newTrans.transY += dy;
    this.setTransformMatrix(newTrans);
  } 

  // Applying Deltas to Scale and Translate transformations
  this.applyScale = function(dscale, x, y){
      //console.log("applyScale : ", dscale, x, y);
    let newTrans = this.getTransformMatrix();
      // added by Peter Hirt
      if(isNaN(ele.width)){ ele.width=3000}
      if(isNaN(ele.height)){ ele.height=1700}
    let tranX = x - (ele.width / 2);
    let tranY = y - (ele.height / 2);
      //console.log("div half width and height : ", tranX, tranY, ele.height, ele.width);
    dscale = (this.liner ? dscale : dscale * (newTrans.scale)) // scale either liner or non-liner 
    newTrans.scale += dscale;
    let maxOrMinScale = (newTrans.scale <= this.minScale || newTrans.scale >= this.maxScale);
    if(newTrans.scale < this.minScale) newTrans.scale = this.minScale;
    if(newTrans.scale > this.maxScale) newTrans.scale = this.maxScale;
    if(!maxOrMinScale) {
      this.applyTranslate(tranX, tranY);
      this.setTransformMatrix(newTrans);
      this.applyTranslate(-(tranX * dscale), -(tranY * dscale));
    }
  }

  // Capture when the mouse is down on the element or not
  ele.addEventListener("mousedown", function(e) {
    e.preventDefault();
    this.panning = true;
    this.oldX = e.clientX;
    this.oldY = e.clientY;
    //console.log("X/Y ccordinates : ", this.oldX, this.oldY, "panning enabled : ", this.panning)
  });
  
  ele.addEventListener("mouseup", function(e) { 
      this.panning = false;
      //console.log("panning enabled : ", this.panning);
  });
  ele.addEventListener("mouseleave", function(e) { 
      this.panning = false; 
      //console.log("panning enabled : ", this.panning);
  });

  ele.addEventListener("mousemove", function(e){
    if(this.panning) {
      let deltaX = e.clientX - this.oldX;
      let deltaY = e.clientY - this.oldY;
      self.applyTranslate(deltaX, deltaY);
      this.oldX = e.clientX;
      this.oldY = e.clientY;
      //console.log("X/Y ccordinates : ", this.oldX, this.oldY)
    }
  });

  this.getScrollDirection = function(e){
    var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
      //console.log("mouse wheel delta : ", delta, " increment : ", self.increment, " X/Y offsets : ", e.offsetX, e.offsetY)
    if(delta < 0)
      self.applyScale(-self.increment, e.offsetX, e.offsetY)
    else
      self.applyScale(self.increment, e.offsetX, e.offsetY);
  }

  //ele.addEventListener('DOMMouseScroll',this.getScrollDirection,false);
  //ele.addEventListener('mousewheel',this.getScrollDirection,false); 
}