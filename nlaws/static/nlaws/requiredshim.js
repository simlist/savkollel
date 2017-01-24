$(function(){
    $('form').submit(function (e) {
        if (!e.target.checkValidity()) {
            $(this).find('[required]').each(function () {
                var self = $(this);
                if (self.val() === '') {
                    e.preventDefault();
                    alert('Please choose a pickup date');
                    self.focus().scrollIntoView(true);
                }
            });
        }
    });
    
});