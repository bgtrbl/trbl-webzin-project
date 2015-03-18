$(function() {
    $(document).on('click', '.trbl_linkForm', function (event) {
        var target= $(this).attr('href'),
            cssCls= $(this).attr('rel');

        $('.modal-content').load(target, function() {
            $('.modal-content').removeClass().addClass('modal-content '+ cssCls);
        });
        event.preventDefault();
    });
});


