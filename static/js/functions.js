function ReportAjaxError(response){
	console.error('错误：');
	console.error(response);
	console.error(response.responseText);
	layer.alert('出锅了，提交失败<br />详细信息请查看控制台。<br />不过，输入的东西应该还在。',{
		title: '错误',
		icon: 2
	})
}
