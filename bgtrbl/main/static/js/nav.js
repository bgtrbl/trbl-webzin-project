$(function() {

    var bodyEl = document.body,
        openbtn = $('.trbl_sideToggle'),
        isOpen = false;

    function init() {
        initEvents();
    }

    function initEvents() {
        $(document).on( 'mouseover touchend', '.trbl_sideToggle' , toggleMenu );
        $(document).on('click', '#close-button', toggleMenu);
        $(document).on( 'click touchend', '#trbl_contents', function(ev) {
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
            $('#trbl_openSlide').hide();

        }
        isOpen = !isOpen;
    }

    init();

});
