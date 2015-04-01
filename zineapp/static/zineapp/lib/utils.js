// ======================= DOM Utility Functions from PastryKit =============================== //

// Sure, we could use jQuery or XUI for these, 
// but these are concise and will work with plain vanilla JS

Element.prototype.hasClassName = function (a) {
    return new RegExp("(?:^|\\s+)" + a + "(?:\\s+|$)").test(this.className);
};

Element.prototype.addClassName = function (a) {
    if (!this.hasClassName(a)) {
        this.className = [this.className, a].join(" ");
    }
};

Element.prototype.removeClassName = function (b) {
    if (this.hasClassName(b)) {
        var a = this.className;
        this.className = a.replace(new RegExp("(?:^|\\s+)" + b + "(?:\\s+|$)", "g"), " ");
    }
};

Element.prototype.toggleClassName = function (a) {
  this[this.hasClassName(a) ? "removeClassName" : "addClassName"](a);
};

// ======================= DDD mini framework =============================== //

(function($){

var DDD = {};
// again, borrowed from PastryKit
DDD.isTangible = !!('createTouch' in document);
DDD.CursorStartEvent = DDD.isTangible ? 'touchstart' : 'mousedown';
DDD.CursorMoveEvent = DDD.isTangible ? 'touchmove' : 'mousemove';
DDD.CursorEndEvent = DDD.isTangible ? 'touchend' : 'mouseup';

// get i.e. 'WebkitTransform'
var transformProp = Modernizr.prefixed('transform');

/* ==================== EventHandler ==================== */

DDD.EventHandler = function() {};

DDD.EventHandler.prototype.handleEvent = function( event ) {
  if ( this[event.type] ) {
    this[event.type](event);
  }
};

/* ==================== Test 3D transform support ==================== */

DDD.translate = Modernizr.csstransforms3d ?
  function( x, y ) {
    return 'translate3d(' + x + 'px, ' + y + 'px, 0 )';
  } :
  function( x, y ) {
    return 'translate(' + x + 'px, ' + y + 'px)';
  };


/* ==================== Start Up ==================== */


DDD.init = function() {
  
  var ranges = document.querySelectorAll('input[type="range"]'),
      rangesLen = ranges.length,
      i;
  
  if ( rangesLen ) {
    
     // create range output display
    for ( i=0; i < rangesLen; i++ ) {
      new DDD.RangeDisplay( ranges[i] );
    }
    
  }
  
};


window.addEventListener( 'DOMContentLoaded', DDD.init, false);

// put in global namespace
window.DDD = DDD;

})(jQuery);

var transformProp = Modernizr.prefixed('transform');

function Carousel3D ( el ) {
  this.element = el;

  this.rotation = 0;
  this.panelCount = 0;
  this.totalPanelCount = this.element.children.length;
  this.theta = 0;

  this.isHorizontal = true;

}

Carousel3D.prototype.modify = function() {

  var panel, angle, i;

  this.panelSize = this.element[ this.isHorizontal ? 'offsetWidth' : 'offsetHeight' ];
  this.rotateFn = this.isHorizontal ? 'rotateY' : 'rotateX';
  this.theta = 360 / this.panelCount;

  // do some trig to figure out how big the carousel
  // is in 3D space
  this.radius = Math.round( ( this.panelSize / 2) / Math.tan( Math.PI / this.panelCount ) );

  for ( i = 0; i < this.panelCount; i++ ) {
    panel = this.element.children[i];
    angle = this.theta * i;
    panel.style.opacity = 1;
    // panel.style.backgroundColor = 'hsla(' + angle + ', 100%, 50%, 0.8)';
    // rotate panel, then push it out in 3D space
    panel.style[ transformProp ] = this.rotateFn + '(' + angle + 'deg) translateZ(' + this.radius + 'px)';
  }

  // adjust rotation so panels are always flat
  this.rotation = Math.round( this.rotation / this.theta ) * this.theta;
  this.transform();

};

Carousel3D.prototype.transform = function() {
  // push the carousel back in 3D space,
  // and rotate it
  this.element.style[ transformProp ] = 'translateZ(-' + this.radius + 'px) ' + this.rotateFn + '(' + this.rotation + 'deg)';
};

Carousel3D.prototype.setDims = function(aspectRatio, percentMargin){
  // aspectRatio of page (height/width) and aim for taking up percentMargin of carousel-container/polygon face
  // Given R = (X/2)/tan(pi/2), and constraint that 2R = V(iewport) to keep it in view

  // TO DO: find a more satisfactory fix than this hack
  n = (this.panelCount > 10) ? 10 : this.panelCount;
  var VtoX = Math.tan( Math.PI/ n );
  VtoX = VtoX < 0.9 ? VtoX : 0.9;

  var Vx = $('.carousel-viewport').width();
  var Vy = $('.carousel-viewport').height();


  $('.carousel-container').width(Vx * VtoX);
  $('.carousel-container').height(Vy * VtoX);

  var yQuery1 = percentMargin * VtoX * Vy;
  var yQuery2 = percentMargin * VtoX * Vx * aspectRatio;
  var x, y;
  if (yQuery1 < yQuery2){
    y = yQuery1;
  } else {
    y = yQuery2;
  }
  x = y / aspectRatio;
  $('figure').css({'width': x+'px', 'height': y+'px'});

  // finally, ensure figure is centred
  $('figure').css({
    'margin-left': -$('figure').width()/2+'px',
    'margin-top': -$('figure').height()/2+'px',
  });
};

var init = function() {

  var carousel = new Carousel3D( document.getElementById('carousel') ),
      panelCountInput = document.getElementById('carousel'),
      axisButton = document.getElementById('toggle-axis'),
      navButtons = document.querySelectorAll('#navigation button'),

      onNavButtonClick = function( event ){
        var increment = parseInt( event.target.getAttribute('data-increment') );
        carousel.rotation += carousel.theta * increment * -1;
        carousel.transform();
      };

  // populate on startup
  carousel.panelCount = panelCountInput.children.length;
  carousel.modify();
  carousel.setDims(1.414, 0.65);

  axisButton.addEventListener( 'click', function(){
    carousel.isHorizontal = !carousel.isHorizontal;
    carousel.modify();
  }, false);


  for (var i=0; i < 2; i++) {
    navButtons[i].addEventListener( 'click', onNavButtonClick, false);
  }

  document.getElementById('toggle-backface-visibility').addEventListener( 'click', function(){
    carousel.element.toggleClassName('panels-backface-invisible');
  }, false);

  setTimeout( function(){
    document.body.addClassName('ready');
  }, 0);

};

window.addEventListener( 'DOMContentLoaded', init, false);
