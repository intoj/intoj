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
	// var lyst = $(".havemarkdown")
	// for( var i = 0 ; i < lyst.length ; ++i ){
	// 	var cur = $(lyst[i])
	// 	cur.html(marked(cur.html()))
	// }
	$(".havemarkdown").each(function(index,cur){
		cur = $(cur)
		cur.html(marked(cur.html()))
	})
}

function AutoFontSize(){
	$(".auto-font-size").each(function(index,cur){
		cur = $(cur)
		cur.css("white-space","nowrap")
		cur.css("font-size","0px")
		var fa = cur.parent()
		var fa_width = parseInt(fa.css("width"))
		var fa_height = parseInt(fa.css("height"))
		var font_size = 8
		function CheckOk(font_size){
			cur.css("font-size",font_size.toString()+"px")
			return Math.max(parseInt(fa.css("width")),parseInt(cur.css("width"))) <= fa_width && font_size <= 19;
		}
		var font_size_l = 8
		var font_size_r = 19
		var max_ok_font_size = 8
		while( font_size_l < font_size_r ){
			var mid = ( font_size_l + font_size_r ) / 2
			if(CheckOk(mid)){
				max_ok_font_size = mid
				font_size_l = mid+1
			}else{
				font_size_r = mid-1
			}
		}
		cur.css("font-size",max_ok_font_size.toString()+"px")
	})
}

function Render(){
	RenderMarkdown()
	AutoFontSize()
}
