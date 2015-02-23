// GLOBAL VARS

// selectors
// TO DO: compact these into a selector object (const)
var contentSelector = '.content';
var viewportSelector = '.flex-container'; // used in moveClose
var containerSelector = '.zine-container';
var flexItemSelector = '.flex-item';
var magazineSelector = '.zine';

// states
var STATES = {};
STATES.DEACTIVATED = 'deactivated'; STATES.DEACTIVATING = 'deactivating';
STATES.ACTIVATED = 'activated'; STATES.ACTIVATING = 'activating';
STATES.ZOOMED = 'zoomed'; STATES.ZOOMING = 'zooming';


// should be combined into a 'moveZine' module
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

// FUNCTIONS
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

        // set position
        container.css(pos);

        // // if this particular container is already mid transition...
        // if (container.hasClass('deactivating') || container.hasClass('activating') || container.hasClass('zooming')){

        //     // ...postpone repositioning till after transition complete
        //     // container.on(transitionEnd,function(){
        //         // applyCalcs();
        //         // container.off(transitionEnd);
        //     // });
        // } else {
        //     // otherwise apply calculations now
        //     // UPDATE TRANSLATION IF ZINE IS ACTIVE
        //     // if window is resized, translation will not be correct to put container in centre
        //     // if (container.hasClass('active')){
        //     //     // update active translation
        //     //     setActiveTranslation(container);
        //     //     // apply updated transform params
        //     //     setTransform(container);
        //     // }
        // }
    });
}

var positionFunc = positionZines;

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
    if (container.hasClass(STATES.ZOOMED)){
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

// design an event handler (on each event 'e' call this function)
// specifically for an active magazine to be controlled by the keyboard
function magKeydownHdlr(e) {
    // get the currently active magazine
    var activeContainer = $(containerSelector + '.' + STATES.ACTIVATED + ', ' +
        containerSelector + '.' + STATES.ZOOMED);
    var activeMag = activeContainer.children(magazineSelector);
    if(activeContainer.exists()){
        switch (e.which) {
            case 37: activeMag.turn('previous'); // left arrow key
                break;
            case 39: activeMag.turn('next'); // right arrow key
                break;
            case 27:
                console.log("triggering");
                $('.zine-container').trigger('deactivate');
                break;
        }
    }
    switch(e.which){
        case 68: debug_message(); // up arrow key
            break;
        // case 40: activeContainer.zoom('zoomOut'); // down arrow key
            // break;
        default: return;
    }
    e.preventDefault();
}

// extend jQuery with 'does selector find anything' function
$.fn.exists = function () {
    return this.length !== 0;
};

var viewport;
// INITIALISATION
$(window).ready(function(){
    // record viewport element
    viewport = $(viewportSelector);
    // set container zineapp is embedded within, to a large size
    viewport.parent().css({'height':'80%','width':'80%'});
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
    // setTimeout(positionZines, 500); // nasty hack to account for fullPage resize delay
    // $(window).resize(function(){
        // setTimeout(positionZines,2000);
    // }); // nasty hack to account for fullPage resize delay

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

    // program state machine behaviour
    $('.zine-container').machine({
        // inactive state
        deactivated: {
            defaultState: true,
            onEnter: function() {
                console.log("> inactive");
            },
            onExit: function() {
                console.log("inactive >");
            },
            events: {
                click: STATES.ACTIVATING,
            }
        },

        // activating state
        activating: {
            onEnter: function() {
                console.log("> activating");
                subject = $(this);

                // deactivate any other zines
                $('.zine-container').each(function(){
                    if(!$(this).hasClass(STATES.DEACTIVATED)){
                        if(!$(this).is(subject)){
                            console.log("not the subject!");
                            $(this).trigger('deactivate');
                        }
                    }
                });

                // TRANFORM PROPERTIES
                // set active translation
                setActiveTranslation($(this));
                // set active scale
                zineTransform.scale = ACTIVE_SCALE_FACTORS;
                // PERFORM CSS TRANSFORM
                setTransform($(this));
            },
            onExit: function() {
                console.log("active >");
            },
            events: {
                transitionend: STATES.ACTIVATED,
                webkitTransitionEnd: STATES.ACTIVATED,
                otransitionend: STATES.ACTIVATED,
                mstransitionend: STATES.ACTIVATED,

                deactivate: STATES.DEACTIVATING,
            }
        },

        // active state
        activated: {
            onEnter: function() {
                // $(this).css({'background-color':'yellow'});
                console.log("> active");
                $(this).children('.nav').addClass('active');
            },
            onExit: function() {
                console.log("active >");
            },
            events: {
                click: STATES.ZOOMING,

                deactivate: STATES.DEACTIVATING,
            },
        },

        // zooming state
        zooming: {
            onEnter: function() {
                console.log("> zooming");

                // TRANSFORM PROPERTIES
                // set active translation
                setActiveTranslation($(this));
                // initialise zoomed translation
                zineTransform.zoomedTranslation = {x: 0, y: 0};
                // increase scale
                zineTransform.scale = ZOOMED_SCALE_FACTORS;
                // PERFORM CSS TRANSFORM
                setTransform($(this));
            },
            onExit: function() {
                console.log("zooming >");
            },
            events: {
                transitionend: STATES.ZOOMED,
                webkitTransitionEnd: STATES.ZOOMED,
                otransitionend: STATES.ZOOMED,
                mstransitionend: STATES.ZOOMED,

                deactivate: STATES.DEACTIVATING,
            },
        },

        // zoomed state
        zoomed: {
            onEnter: function() {
                console.log("> zoomed");
            },
            onExit: function() {
                console.log("zoomed >");
            },
            events: {
                click: STATES.ACTIVATING,
                deactivate: STATES.DEACTIVATING,
            },
        },

    // deactivating state
    deactivating: {
            onEnter: function() {
                console.log("> deactivating");

                $(this).children('.nav').removeClass('active');

                // TRANSFORM PROPERTIES
                // apply no translation from original position
                zineTransform.activeTranslation = {x: 0, y: 0};
                // scale down to original, small size 
                zineTransform.scale = {x: 1, y: 1};
                // PERFORM CSS TRANSFORM
                setTransform($(this));
            },
            onExit: function() {
                console.log("deactivating >");
            },
            events: {
                transitionend: STATES.DEACTIVATED,
                webkitTransitionEnd: STATES.DEACTIVATED,
                otransitionend: STATES.DEACTIVATED,
                mstransitionend: STATES.DEACTIVATED,
            },
        },

    }, {setClass: true});
});

// DEBUGGING
 
function debug_message(){
    $('.zine-container').each(function(){
        container = $(this);
        var centrePos = {
            x: parseInt(container.css('left')) + parseInt(container.css('width')) / 2,
            y: parseInt(container.css('top')) + parseInt(container.css('height')) / 2,
        };
        at = zineTransform.activeTranslation;
        console.log("Classes: [" + $(this).attr('class') +
            "], anchor pos: " + JSON.stringify(centrePos));
    });
    console.log("active translation: " + JSON.stringify(zineTransform.activeTranslation));
}