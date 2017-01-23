$(function(){
    if (!('required' in document.createElement('input'))) {
        $('form').on('submit', function (e) {
            $('[required]').each(function () {
                var self = $(this);
                if (self.val() === '') { e.preventDefault(); self.focus(); }
            });
        });
    }
});