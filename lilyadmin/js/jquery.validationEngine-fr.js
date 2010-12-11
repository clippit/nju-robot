

(function($) {
	$.fn.validationEngineLanguage = function() {};
	$.validationEngineLanguage = {
		newLang: function() {
			$.validationEngineLanguage.allRules = {"required":{    
						"regex":"none",
						"alertText":"此项不能为空",
						"alertTextCheckboxMultiple":"*Choisir un option",
						"alertTextCheckboxe":"* Ce checkbox est requis"},
					"length":{
						"regex":"none",
						"alertText":"* Entre ",
						"alertText2":" et ",
						"alertText3":" caractères requis"},
					"minCheckbox":{
						"regex":"none",
						"alertText":"* Nombre max the boite exceder"},	
					"confirm":{
						"regex":"none",
						"alertText":"* Votre champs n'est pas identique"},		
					"telephone":{
						"regex":"/^[0-9\-\(\)\ ]+$/",
						"alertText":"* Numéro de téléphone invalide"},	
					"email":{
						"regex":"/^[a-zA-Z0-9_\.\-]+\@([a-zA-Z0-9\-]+\.)+[a-zA-Z0-9]{2,4}$/",
						"alertText":"E-mail格式不正确, 请检查"},	
					"date":{
                         "regex":"/^[0-9]{4}\-\[0-9]{1,2}\-\[0-9]{1,2}$/",
                         "alertText":"日期格式不正确，格式应该为： YYYY-MM-DD"},
					"onlyNumber":{
						"regex":"/^[0-9\ ]+$/",
						"alertText":"此项只能填入数字"},	
					"noSpecialCaracters":{
						"regex":"/^[0-9a-zA-Z]+$/",
						"alertText":"此项只能填入数字和字母"},	
					"onlyLetter":{
						"regex":"/^[a-zA-Z\ \']+$/",
						"alertText":"此项只能填入字母"}
				}	
		}
	}
})(jQuery);

$(document).ready(function() {	
	$.validationEngineLanguage.newLang()
});