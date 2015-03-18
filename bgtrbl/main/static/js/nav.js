$(function() {

    var bodyEl = document.body,
        content = document.querySelector( '#trbl_contents' ),
        closebtn = document.getElementById( 'close-button' ),
        isOpen = false;

    function init() {
        initEvents();
    }

    function initEvents() {
        $(document).on( 'click', '.trbl_sideToggle' , toggleMenu );
        if( closebtn ) {
            closebtn.on( 'click', toggleMenu );
        }

        $(document).on( 'click', '#trbl_contents', function(ev) {
            var target = ev.target;
            if( isOpen && target !== openbtn ) {
                toggleMenu();
            }
        } );
    }

    function toggleMenu() {
        if( isOpen ) {
            classie.remove( bodyEl, 'show-menu' );
            $('#trbl_openSlide').show();
        }
        else {
            classie.add( bodyEl, 'show-menu' );
            $(this).hide();

        }
        isOpen = !isOpen;
    }

    init();

});
