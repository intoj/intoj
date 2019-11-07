function ReportAjaxError(response){
	console.error('错误：');
	console.error(response);
	console.error(response.responseText);
	layer.alert('出锅了，提交失败<br />详细信息请查看控制台。<br />不过，输入的东西应该还在。',{
		title: '错误',
		icon: 2
	})
}

// by W3school, https://www.w3school.com.cn/js/js_cookies.asp
// modified
function GetCookie(cname){
	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');
	for( var i = 0 ; i < ca.length ; i++ ){
		var c = ca[i];
		while( c.charAt(0) == ' ' ){
			c = c.substring(1);
		}
		if( c.indexOf(name) == 0 ){
			return c.substring(name.length,c.length);
		}
	 }
	return "";
}
