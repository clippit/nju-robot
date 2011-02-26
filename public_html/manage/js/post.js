$(document).ready(init);
var w_sbox = null;
var c_sbox = null;
var items = new Array('abraham', 'aptana');
function init(){

    $("#btn_submit").bind("click", submitPost);
    
    
    $("input").bind("focus", function(){
        this.select();
    });
    
    $("#_title").bind("blur", function(){
        if (this.value.trim() == "") {
            showErrorTip("e_title","标题不能为空！","error_tip");
        }else{
			$("#e_title").remove();
		}
    });
    
    init_suggest_box();
    
    
}

function init_suggest_box(){
    var w_ibox = get$("w_aid");
    w_sbox = new SuggestBox(get$('w_suggest'), w_ibox, w_ibox.offsetLeft, w_ibox.offsetTop + w_ibox.offsetHeight, w_ibox.offsetWidth, 16);
    w_sbox.addEvent("selecteditemchange", w_dealSelectedItemChange);
    
    $("#w_aid").bind("keyup", deal_w_suggest).bind("blur", function(){
        var text = this.value.trim();
        if (text != "") {
            var city = getFirstMatchCity(text);
            if (city !== null) {
                addCity(city);
                this.value = "";
            }
            else {
                showErrorTip("e_w_aid","不能识别的城市名。","error_tip");
            }
        }
        else {
            if (selCity.length === 0) {
                showErrorTip("e_w_aid","至少选择一个城市。","error_tip");
            }
        }
        
    });
    
    
    var c_ibox = get$("company");
    c_sbox = new SuggestBox(get$("c_suggest"), c_ibox, c_ibox.offsetLeft, c_ibox.offsetTop + c_ibox.offsetHeight, c_ibox.offsetWidth, 16);
    c_sbox.addEvent("selecteditemchange", c_dealSelectedItemChange);
    $("#company").bind("keyup", deal_company_suggest).bind("blur", function(){
        if (this.value.trim() == "") {
			  showErrorTip("e_company","公司名称不能为空。","error_tip");
        }else{
			$('#e_company').remove();
		}
    });
}

var selCity = new Array();
function getCitySelectedIndex(cid){
    for (var i = 0; i < selCity.length; i++) 
        if (cid == selCity[i]) 
            return i;
    return -1;
}

function w_dealSelectedItemChange(arg){
    var id = arg.index;
    var city = suggestCity[id];
    if (addCity(city) == "existed") {
        alert("地点：" + cname + " 已经选择过了，不能重复选择！");
    }
    get$('w_aid').value = "";
    get$('w_aid').focus();
    
}

function addCity(city){
    var cname = getCityFullName(city);
    if (getCitySelectedIndex(city.id) === -1) {
        selCity.push(city.id);
        var d = $('<div/>').attr({
            'id': city.id,
            'class': 'line_c'
        }).html('<p>' + cname + '</p>').appendTo(get$('w_lists'));
        $('<a/>').attr('id', 'del_' + city.id).attr('href', 'javascript:deleteCity(' + city.id + ');').html("<img src='images/delete.gif'/>").appendTo(d);
        return "added";
    }
    else {
        return "existed";
        
    }
    
}

var suggestCity = null;
function deal_w_suggest(data){
    if (data.keyCode == 38 || data.keyCode == 40) 
        if (w_sbox.getVisible() == true) 
            return;
    
    var text = this.value.trim();
    if (text == '') {
        w_sbox.close();
        return;
    }
    suggestCity = getCitySuggest(text);
    var len = suggestCity.length;
    if (len == 0) {
        w_sbox.close();
    }
    else {
        var cities = new Array();
        for (var i = 0; i < len; i++) {
            var s = suggestCity[i];
            var value=getCityFullName(s);         
            cities.push(value);
        }
        
        w_sbox.showItems(cities);
    }
}



function submitPost(){
    if (!validateInput()) 
        return;
    var description = editor.document.getBody().getText().substr(0, 99).trim();
    if (description == "") {//msg.replace(/<[^<>]+>/g,'').replace(/&nbsp[;]/g,'').replace(/\s+/g,'')=='') {
        alert('招聘信息内容不能为空！');
        return;
    }
    else {
        get$("description").value = description;
    }
    alert(description);
    get$("form_1").submit();
}

function c_dealSelectedItemChange(arg){
    c_change = false;
    get$("company").value = arg.name;
}

var c_change = true;
function deal_company_suggest(data){
    if (data.keyCode == 38 || data.keyCode == 40) 
        if (c_sbox.getVisible() == true) 
            return;
    if (data.keyCode == 13) {
        return;
    }
    var text = this.value.trim();
    if (text == '') {
        c_sbox.close();
        return;
    }
    if (c_change === false) {
        c_change = true;
        return;
    }
    $.post("companySuggest.php", {
        "text": text
    }, function(data){
        var items = eval(data);
        c_sbox.showItems(items);
    });
    
}

function showErrorTip(id, msg, parent_id){
    $("#" + id).remove();
    $("<p id='" + id + "' />").html(msg).appendTo(get$(parent_id));
}

function deleteCity(id){
	selCity= jQuery.grep(selCity, function(value) {
        return value != id;
      });
	  $('#'+id).remove();
}
