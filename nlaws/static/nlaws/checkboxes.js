$(function(){
	$('div.checkbox input').change(function(){
    var checkbox = $(this);
		var hidden_div = checkbox.closest('div.checkbox').next('div');
		if(checkbox.is(':checked')){
		  hidden_div.removeClass('hidden');
		  hidden_div.find('input').removeAttr('disabled');
		}
		else{
			hidden_div.addClass('hidden');
      hidden_div.find('input').attr('disabled', 'disabled');
		}
	});
}
);
