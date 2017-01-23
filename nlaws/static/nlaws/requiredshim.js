$(function(){
    $('form').submit(function (e) {
        if (!e.target.checkValidity()) {
            $('.required').each(function () {
                var self = $(this);
                if (self.val() == '') { e.preventDefault(); self.focus(); alert('Please choose the pickup date')}
            });
        }
    });
    
});