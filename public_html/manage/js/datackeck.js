/**
 * 
 */
$(document).ready(init);
function init(){
    $("#publish").bind("click", submitPost);
    
    $("input").bind("focus", function(){
        this.select();
    });
    $("#post_title").bind("blur", function(){
        if (this.value.trim() == "") {
            showErrorTip("post_title","标题不能为空！","error_tip");
        }else{
			$("#post_title").remove();
		}
    });
}

function showErrorTip(id, msg){
//  $("#" + id).remove();
	alert("#" + id);
	$("#" + id).css({
		'color':'#5F7A77'
	});
//    $("<p id='" + id + "' />").html(msg).appendTo(get$(parent_id));
}

function submitPost(){
	
	return false;
}