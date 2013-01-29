

// add photo from map highlight
$('map .photo-input').click(function(e){
	// get the id of this thing
	var interview_id = $(this).attr('id');

	// initiate photo adding process
	views.addInterviewPhoto(interview_id);

});

// allow for location dragging
$('.location-base').mousedown(function(e){
	// initiate move
	feature = $(this).parent('g');
	// raise from base
	// add dragging class
	feature.toggleClass('dragging');
}).mousemove(function(e){
	// if dragging
	if (feature.hasClass('dragging')){
		// follow mouse
		var mouseX = null;
		var mouseY = null;
		feature.attr('transform',
			'translate('+mouseX+', '+mouseY+')');
	}
}).mouseup(function(e){
	// if dragging
	if (feature.hasClass('dragging')){
		// get new location
		var mouseX = null;
		var mouseY = null;
		// convert the location to lat long
		var latlon = new MM.Point(mouseX, mouseY);
		//click and drag the interview
		views.moveLocation(loc_id, latlon);
		// remove the dragging state
		feature.toggleClass('dragging');
	}
});





