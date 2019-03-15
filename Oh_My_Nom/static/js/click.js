$('#likes').click(function(){
	var catid;
	catid = $(this).attr("data-catid");
	$.get('/randomrecipes/', {category_id: catid}, function(data){
	$('#like_count').html(data);
	$('#likes').hide();
	});
});
