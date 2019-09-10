function RenderMarkdown(){
	marked.setOptions({
		renderer: new marked.Renderer(),
		gfm: true,
		tables: true,
		escaped : true,
		breaks: false,
		pedantic: false,
		smartLists: true,
		smartypants: false,
		xhtml: true,
		sanitize: false,
		highlight: function(code,lang){
			if( lang == "plain" ){
				return "<code class=\"hljs plaintext\">" + code + "</code>"
			}
			return "<code class=\"hljs "+lang+"\" style=\"padding: 0 !important;\">" + code + "</code>"
		}
	});
	var lyst = $(".havemarkdown")
	for( var i = 0 ; i < lyst.length ; ++i ){
		var cur = $(lyst[i])
		cur.html(marked(cur.html()))
	}
}
function Render(){
	RenderMarkdown()

}
