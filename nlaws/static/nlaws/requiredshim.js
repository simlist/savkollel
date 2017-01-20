$(function () {
    if (!('required' in document.createElement('input'))) {
        $('form').submit(function (e) {
            $('[required]').each(function () {
                if ($(this).val() === '') { e.preventDefault(); }
            });
        });
    }

});