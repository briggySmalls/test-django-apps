/* Magazine sample */

(function($) {

zine = function(sampleName, samplePath, pageCount){

    // ensure sample path ends with a /
    if(samplePath.charAt(samplePath.length-1) !== '/'){
        samplePath += '/';
    }

    // add some dynamic css styles that we cannot put in static .css file
    var picsUrl = samplePath + 'pics/';
    $("<style type='text/css'>" +
        ".bookshelf ." + sampleName + "-thumb,.bookshelf-row ." + sampleName + "-thumb{" +
        "background-image:url('" + picsUrl + "thumb.jpg');}" +
        "</style>").appendTo("body");

    function addPage(page, book) {

        var id, pages = book.turn('pages');
        var hardPages = [1, 2, pageCount - 1, pageCount];
        var classes = (hardPages.indexOf(page) > -1) ? 'hard' : '';
        var element = $('<div />', {}).addClass(classes);

        if (book.turn('addPage', element, page)) {
            element.html('<div class="gradient"></div><div class="loader"></div>');
            loadPage(page);
        }
    }

    // function that gives impressions of pages stacking (using page-depth.jpg)
    function updateDepth(book, newPage) {

        var page = book.turn('page'),
            pages = book.turn('pages'),
            depthWidth = 16*Math.min(1, page*2/pages);

            newPage = newPage || page;

        if (newPage>3)
            $('.sam-test .p2 .depth').css({
                width: depthWidth,
                left: 20 - depthWidth
            });
        else
            $('.sam-test .p2 .depth').css({width: 0});

            depthWidth = 16*Math.min(1, (pages-page)*2/pages);

        if (newPage<pages-3)
            $('.sam-test .p111 .depth').css({
                width: depthWidth,
                right: 20 - depthWidth
            });
        else
            $('.sj-book .p111 .depth').css({width: 0});

    }

    function loadPage(page) {

        var img = $('<img />');
        img.load(function() {
            var container = $('.sam-test .p'+page);
            img.css({width: '100%', height: '100%'});
            img.appendTo($('.sam-test .p'+page));
            container.find('.loader').remove();
        });

        img.attr('src', samplePath + 'pages/' +  page + '.jpg');

    }

    function loadLargePage(page, pageElement) {

        var img = $('<img />');

        img.load(function() {

            var prevImg = pageElement.find('img');
            $(this).css({width: '100%', height: '100%'});
            $(this).appendTo(pageElement);
            prevImg.remove();

        });

        img.attr('src', samplePath + 'pages/' +  page + '-large.jpg');
    }

    function loadSmallPage(page, pageElement) {

        var img = pageElement.find('img');

        img.css({width: '100%', height: '100%'});

        img.unbind('load');

        img.attr('src', samplePath + 'pages/' +  page + '.jpg');
    }

    function zoomTo(event) {

        if ($(this).zoom('value')==1)
            $(this).zoom('zoomIn', event);
        else
            $(this).zoom('zoomOut');

    }


    function loadFlipbook(flipbook) {

        if (flipbook.width()===0) {

            if (bookshelf.currentSampleName()==sampleName) {
                setTimeout(function() {
                    loadFlipbook(flipbook);
                }, 10);
            }

            return;
        }

        flipbook.turn({
            acceleration: !isChrome(),
            gradients: true,
            autoCenter: true,
            duration: 1000,
            pages: pageCount,
            when: {

            turning: function(e, page, view) {

                var book = $(this),
                currentPage = book.turn('page'),
                pages = book.turn('pages');

                if (!$('.splash .bookshelf').is(':visible'))
                    Hash.go('samples/' + sampleName+'/'+page).update();


                if (page==1)
                    $('.previous-button').hide();
                else
                    $('.previous-button').show();


                if (page==pages)
                    $('.next-button').hide();
                else
                    $('.next-button').show();

                updateDepth(book, page);

            },

            turned: function(e, page, view) {

                var book = $(this);

                $('#slider').slider('value', getViewNumber(book, page));

                if (page!=1 && page!=book.turn('pages'))
                    $('sam-test .tabs').fadeIn(500);


                book.turn('center');

            },

            start: function(e, pageObj) {

                bookshelf.moveBar(true);

            },

            end: function(e, pageObj) {

                var book = $(this);

                setTimeout(function() {
                    $('#slider').slider('value', getViewNumber(book));
                }, 1);

                bookshelf.moveBar(false);

            },

            missing: function (e, pages) {

                for (var i = 0; i < pages.length; i++)
                    addPage(pages[i], $(this));

            }
        }
    });

        // Zoom
        $('.splash').zoom({
            flipbook: flipbook,

            max: function() {

                return 2.4;

            },

            when: {
                resize: function(event, scale, page, pageElement) {

                    if (scale==1)
                        loadSmallPage(page, pageElement);
                    else
                        loadLargePage(page, pageElement);

                },

                change: function(event, scale) {

                    if (scale==1) {

                        $('.splash').addClass('no-transition').height('');
                        // $('body > :not(.splash)').show();
                        $('.bar').css({visibility:'visible'});
                        $('#slider-bar').css({visibility:'visible'});
                        bookshelf.zoomOutButton(false);

                    } else {

                        $('sam-test').removeClass('animated').addClass('zoom-in');
                        $('.splash').addClass('no-transition').height($(window).height());
                        // $('body > :not(.splash)').hide(); TO DO: hide window scrollbar when zoomed

                    }

                },

                zoomIn: function () {

                    $('.bar').css({visibility:'hidden'});
                    $('#slider-bar').css({visibility:'hidden'});
                    bookshelf.zoomOutButton(true);

                },

                zoomOut: function () {

                    setTimeout(function(){
                        $('sam-test').addClass('animated').removeClass('zoom-in');
                    }, 0);

                },

                swipeLeft: function() {

                    $('sam-test').turn('next');

                },

                swipeRight: function() {

                    $('sam-test').turn('previous');

                }
            }
        });

        if ($.isTouch)
            $('.splash').bind('zoom.doubleTap', zoomTo);
        else
            $('.splash').bind('zoom.tap', zoomTo);

        $('#slider').slider('option', 'max', numberOfViews(flipbook));

        flipbook.addClass('animated');
    }

    ////////////

    bookshelf.loadSample(sampleName, function(action) {
        // callback performed each time sample is opened
        var sample = this;

        bookshelf.preloadImgs(['1.jpg'], samplePath + 'pages/',
        function() {

        bookshelf.loaded(sampleName);

        if (action=='preload') {
            return;
        }

        sample.previewWidth = 112;
        sample.previewHeight = 73;
        sample.previewSrc = samplePath + 'pics/preview.jpg';
        sample.tableContents = 3;
        sample.shareLink = 'http://' + location.host + '/#'+samplePath;
        sample.shareText = 'Turn.js: Make a flipbook with HTML5 via @turnjs';


        // Report that the flipbook is loaded
        if (!sample.flipbook) {

            var bookClass = (Modernizr.csstransforms) ?
                'mag1-transform sam-test' :
                'sam-test';

            sample.flipbook = $('<div />', {'class': bookClass}).
                html(
                    '<div ignore="1" class="next-button"></div>' +
                    // '<div depth="5" class="hard"> <div class="side"></div> </div>' +
                    // '<div depth="5" class="hard front-side"> <div class="depth"></div> </div>' +
                    // '<div class="own-size zoom-this"></div>' +
                    // '<div class="own-size even"></div>' +
                    '<div ignore="1" class="previous-button"></div>'
                ).
                appendTo($('#book-zoom'));


            sample.flipbook.find('.next-button').mouseover(function() {
                $(this).addClass('next-button-hover');
            }).mouseout(function() {
                $(this).removeClass('next-button-hover');
            }).mousedown(function() {
                $(this).addClass('next-button-down');
                return false;
            }).mouseup(function() {
                $(this).removeClass('next-button-down');
            }).click(function() {
                sample.flipbook.turn('next');
            });

            sample.flipbook.find('.previous-button').mouseover(function() {
                $(this).addClass('previous-button-hover');
            }).mouseout(function() {
                $(this).removeClass('previous-button-hover');
            }).mousedown(function() {
                $(this).addClass('previous-button-down');
                return false;
            }).mouseup(function() {
                $(this).removeClass('previous-button-down');
            }).click(function() {
                sample.flipbook.turn('previous');
            });

            loadFlipbook(sample.flipbook);

        }
            sample.flipbook.turn("display", isSmall() ? "single" : "double");
            sample.flipbook.turn("size", isSmall() ? 461 : 922, 600);
            bookshelf.showSample();
        });

    });
};
})(jQuery);