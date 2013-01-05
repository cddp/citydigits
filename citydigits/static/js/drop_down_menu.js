$(".pull-handle").hover(function(e){
	// make the .png highlighted
	var img = $(".pull-handle img");
	var new_img = img.attr("src").replace("white", "hover");
	img.attr("src", new_img)
}).click(function(e){
	// slide-collapse the menu columns, leaving only the handle
	$(".pull-down-menu .columns").slideToggle();
});




