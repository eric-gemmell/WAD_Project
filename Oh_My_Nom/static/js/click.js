$('#save-recipe').click(function(){
    var recid;
    recid = $(this).attr("data-recid");
    $.get('/main/save_recipe', {"recipe_id": recid}, function(data){
               $('#save-recipe').hide();

    });
    window.alert("Recipe saved!");
});
