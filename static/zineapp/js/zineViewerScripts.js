// GLOBAL VARS
var viewport = $('.flex-container'); // used in moveClose
var containerSelector = '.zine-container';
var flexItemSelector = '.flex-item';
var magazineSelector = '.zine';

// sould be combined into a 'moveZine' module
var ACTIVE_SCALE_FACTORS = {x: 5, y: 5}; // holds scaling to icon size info. used in moveClose
var ZOOMED_SCALE_FACTORS = {x: 10, y: 10}; // holds scaling to icon size info. used in moveClose

var transitionEnd = 'transitionend webkitTransitionEnd otransitionend mstransitionend';

// zineTransform is relative to actual position
var zineTransform = {
	scale: {x: undefined, y: undefined},
	activeTranslation: {x: undefined, y: undefined},
	zoomedTranslation: {x: undefined, y: undefined},
};
// if put into 'moveZine' module remember to update in positionZines via public method!

// should be combined into a 'zoomZine' module
var viewportOffset = viewport.offset();
// if put into 'zoomZine' module remember to update in positionZines via public method!

// FUNCTIONS

// auto namespace transitionend
function transitionEndName(namespace){
	// save all css transitionend callbacks as one name
	var transitionEndNamespaced = transitionEnd.replace(/ /g,'.' + namespace + ' ');
	return transitionEndNamespaced;
}


function positionZines(){
	// Set zine-containers positions to that of corresponding flex-item
	$(containerSelector).each(function(){
		container = $(this);

		// PERFORM CALCULATIONS
		// build selector
		var sel = '#' + container.attr('id') + flexItemSelector;
		// get corresponding flex-item
		var flexEl = $(sel);
		// get position and account for margin
		var pos = flexEl.position();
		pos.left += parseInt(flexEl.css('margin-left'));
		pos.top += parseInt(flexEl.css('margin-top'));

		var applyCalcs = function(){
			// set position
			container.css(pos);
			// UPDATE TRANSLATION IF ZINE IS ACTIVE
			// if window is resized, translation will not be correct to put container in centre
			if (container.hasClass('active')){
				// update active translation
				setActiveTranslation(container);
			    // apply updated transform params
			    setTransform(container);
			}
		};

		// if this particular container is already mid transition...
		if (container.hasClass('deactivating') || container.hasClass('activating') || container.hasClass('zooming')){
			// find transition namespace
			var namespace;
			if (container.hasClass('deactivating')){
				namespace = 'deactivating';
			} else if (container.hasClass('activating')){
				namespace = 'activating';
			} else if (container.hasClass('zooming')){
				namespace = 'zooming';
			}

			// ...postpone repositioning till after transition complete
			container.on(transitionEnd,function(){
				applyCalcs();
				container.off(transitionEnd);
			});
		} else {
			// otherwise apply calculations now
			applyCalcs();
		}
	});
}

function setActiveTranslation(container){
	// NOTE: jquery's position() and width/height functions return values for transformed
	// element so use .css() function instead
	// NOTE: getting css before transition has finished will give you the wrong values
	var centrePos = {
		x: parseInt(container.css('left')) + parseInt(container.css('width')) / 2,
		y: parseInt(container.css('top')) + parseInt(container.css('height')) / 2,
	};

	 // distance from container centre to viewport centre
	zineTransform.activeTranslation.x = viewport.width() / 2 - centrePos.x;
    zineTransform.activeTranslation.y = viewport.height() / 2 - centrePos.y;
}

function setTransform(container){
	// determine updated transform params
	var translation = zineTransform.activeTranslation; // always apply active translation
	// if the zine is also zoomed...
	if (container.hasClass('zoomed')){
		// ...include the zoomed translation also
		translation.x += zineTransform.zoomedTranslation.x;
		translation.y += zineTransform.zoomedTranslation.y;
	}

    // apply updated transform params
    container.css({
    	"transform": "translate(" + translation.x + "px," + translation.y + "px) " +
        "scale(" + zineTransform.scale.x + "," + zineTransform.scale.y + ")" // std
    });
}

// function to perform css transform
function moveZine(container,state) {
	var transitionEventTag;
	switch (state){
		case 'active':
		// IF TRANSFORMING FROM INACTIVE or ZOOMED TO READING
		
		// UNDO PREVIOUS STATUS
		// indicate zine is not inactive (if it was)
		container.removeClass('inactive');
		// indicate zine is not zoomed (if it was)
		// TO DO: make this a small helper function
		container.removeClass('zoomed');
		container.off('drag');
		container.off('dragend');

		// INDICATE INTERMEDIATE STATUS
		container.addClass('activating');

		// SET STATE FOR UPCOMING STATUS
		transitionEventTag = transitionEndName('activating');
		container.on(transitionEventTag,function(){
			// once css transition has completed.
			// NOTE: THIS COULD BE DUE TO RESIZING! DELAY THAT TRANSITION!
			// signal status
			container.removeClass('activating').addClass('active');
			// setup next click behaviour
			container.one('click',function(){
				// if clicked in active state, zoom
				moveZine(container,'zoomed');
			});
			// unbind the transition event BY NAMESPACE
			// (only removes 'activating' transitions)
			container.off(transitionEventTag);
		});

		// TRANFORM PROPERTIES
		// set active translation
		setActiveTranslation(container);
		// set active scale
    	zineTransform.scale = ACTIVE_SCALE_FACTORS;

		break;
		case 'zoomed':
		// IF ZOOMING IN FROM ACTIVE TO ZOOMED

		// UNDO PREVIOUS STATUS
		// nothing relevant to do here yet...

		// INDICATE INTERMEDIATE STATUS
		container.addClass('zooming');

		// SET STATE FOR UPCOMING STATUS
		transitionEventTag = transitionEndName('zooming');
		container.on(transitionEventTag,function(){
			// once css transition has completed.
			// NOTE: THIS COULD BE DUE TO RESIZING! DELAY THAT TRANSITION!
			// signal status
			container.removeClass('zooming').addClass('zoomed');

			// bind 'drag' event to translation
			container.drag(zoomDragHdlr);
			// update moved-to position at dragend
			container.on('dragend',zoomDragendHdlr);

			// setup next click behaviour
			container.one('click',function(){
				// if clicked in zoomed state, return to active
				moveZine(container,'active');
			});
			// unbind the transition event BY NAMESPACE
			// (only removes 'zoominging' transitions)
			container.off(transitionEventTag);
		});

		// TRANSFORM PROPERTIES
		// initialise zoomed translation
		zineTransform.zoomedTranslation = {x: 0, y: 0};
		// increase scale
		zineTransform.scale = ZOOMED_SCALE_FACTORS;

		break;
		case 'inactive':
		// IF TRANSFORMING FROM READING TO ICON

	    // UNDO PREVIOUS STATUS
		// indicate zine is not active
		container.removeClass('active');
		// indicate zine is not zoomed (if it was)
		container.removeClass('zoomed');
		container.off('drag');
		container.off('dragend');

		// INDICATE INTERMEDIATE STATUS
		container.addClass('deactivating');

		// SET STATE FOR UPCOMING STATUS
		transitionEventTag = transitionEndName('deactivating');
		container.on(transitionEventTag,function(){
			// once css transition has completed.
			// NOTE: THIS COULD BE DUE TO RESIZING! DELAY THAT TRANSITION!
			// signal status
			container.removeClass('deactivating').addClass('inactive');
			// setup next click behaviour
			container.one('click',function(){
				// if clicked in inactive state, activate
				moveZine(container,'active');
			});
			// unbind the transition event BY NAMESPACE
			// (only removes 'deactivating' transitions)
			container.off(transitionEventTag);
		});

	    // TRANSFORM PROPERTIES
    	// apply no translation from original position
    	zineTransform.activeTranslation = {x: 0, y: 0};
    	// scale down to original, small size 
		zineTransform.scale = {x: 1, y: 1};

		break;
	}

    // PERFORM CSS TRANSFORM
    setTransform(container);
}

function zoomDragHdlr(ev,dd) {
	var zoomedContainer = $(containerSelector + '.zoomed');

	// delta signifies distance moved SINCE MOUSEDOWN (so original translation is const offset)
	var offset = {x: dd.deltaX, y: dd.deltaY}; // initially set offset as drag

	// TO DO: CALCULATE IF DRAG WOULD PUT ZINE BOUNDARIES INTO VIEWPORT
	// var zinePos = zoomedContainer[0].getBoundingClientRect(); // handy command to return TRANSFORMED bounds
	// deal with x
	// if (zinePos.left + dd.deltaX > viewportOffset.left){
	// 	// if left edge would be outside of bounds
	// 	offset.x = viewportOffset.left - zinePos.left;
	// } else if (zinePos.right + dd.deltaX < viewportOffset.right){
	// 	// if right edge would be outside of bounds
	// 	offset.x = viewportOffset.right - zinePos.right;
	// }
	// // deal with y
	// if (zinePos.top + dd.deltaY > viewportOffset.top){
	// 	// if top edge would be outside of bounds
	// 	offset.y = viewportOffset.top - zinePos.top;
	// } else if (zinePos.bottom + dd.deltaY < viewportOffset.bottom){
	// 	// if bottom edge would be outside of bounds
	// 	offset.y = viewportOffset.bottom - zinePos.bottom;
	// }
	// 
	translate = {
		x: zineTransform.activeTranslation.x + zineTransform.zoomedTranslation.x + offset.x,
		y: zineTransform.activeTranslation.y + zineTransform.zoomedTranslation.y + offset.y,
	};
	
	// PERFORM CSS TRANSFORM
    zoomedContainer.css({
        // jquery 1.8 and higher will auto-detect browser and provide the right prefix
        "transform": "translate(" + translate.x + "px," +
        	translate.y + "px) " +
        "scale(" + zineTransform.scale.x + "," +
        zineTransform.scale.y + ")"
    });
}

function zoomDragendHdlr(ev,dd){
	// get movement of entire drag operation
	var offset = {x: dd.deltaX, y: dd.deltaY}; // initially set offset as drag
	// update zineTransform with new origin
	zineTransform.zoomedTranslation.x += offset.x;
	zineTransform.zoomedTranslation.y += offset.y;
}

function zoomZine(container){
	// reposition/scale zine
	moveZine(container,'zoomed');

	// after transisioning, mark the zine as in zoomed state
	// NOTE: transitions are turned off in zoomed state
	// TO DO: turn this off when not active!!!
	// container.one('transitionend webkitTransitionEnd oTransitionEnd otransitionend MSTransitionEnd', 
	// 	function() {
	// 		container.addClass('zoomed');
	// 	});

	// bind 'drag' event to translation
	container.drag(zoomDragHdlr);
	// update moved-to position at dragend
	container.on('dragend',zoomDragendHdlr);
}

// design an event handler (on each event 'e' call this function)
// specifically for an active magazine to be controlled by the keyboard
function magKeydownHdlr(e) {
    // get the currently active magazine
    var activeContainer = $(containerSelector + '.active');
    var activeMag = activeContainer.children(magazineSelector);
    try {
        switch (e.which) {
            case 37: activeMag.turn('previous'); // left arrow key
                break;
            case 39: activeMag.turn('next'); // right arrow key
                break;
            case 27: moveZine(activeContainer,'inactive'); // esc key
                break;
            case 38: printClasses(); // up arrow key
            	break;
            // case 40: activeContainer.zoom('zoomOut'); // down arrow key
                // break;

            default: return;
        }
    } catch (err) {
        console.log("tried to process a keydown " + e.which + ". " + err);
    }
    e.preventDefault();
}

// extend jQuery with 'does selector find anything' function
$.fn.exists = function () {
    return this.length !== 0;
};

// DEBUGGING
 
function printClasses(){
    $('.zine-container').each(function(){
        var id = $(this).attr('id');
        var sel = '#' + id + '.disp';
        $(sel).html($(this).attr("class").toString());
    });
}

// INITIALISATION

// set viewport to desired height (proportionately to container) USE CSS INSTEAD (%)
// viewport.height(viewport.parent().height() * 0.8);

// Set flex-items to the correct size to correspond to zine-containers
$(containerSelector).each(function(){
	// build selector
	var sel = '#' + $(this).attr('id') + flexItemSelector;
	// get corresponding flex-item
	var flexEl = $(sel);
	// set flex-items to be same size (to propose relevant positions)
	flexEl.width($(this).width());
	flexEl.height($(this).height());
});

// position zine-containers over corresponding flex-box, always.
positionZines();
$( window ).resize(positionZines);

// initialise zines
$('.zine').each(function(){
	$(this).turn({
	    width: 100,
	    height: 75,
	    autoCenter: true,
	});
});

// bind keydown events
$(window).keydown(magKeydownHdlr);

// set up initial click behaviour
$(containerSelector).each(function(){
	// '.one()' only fires once, thus this is gauranteed to be inactive to active
	$(this).one('click',function(){
		// if another zine is active...
		if($(containerSelector + '.active').exists()){
			// ...deactivate it
			moveZine($(containerSelector + '.active'),'inactive');
		}
		// active this zine for the first time
		moveZine($(this),'active');
	});
});