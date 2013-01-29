
var Views = function(){
	var views = {};
                   
	// audio views
	views.addAudioAnswer = function(interview_id, question_id){
		// go to interview view, and question
		// initiate input (use device )
		alert('add an audio track as an answer to this question');
	};
	views.addAudioTrack = function(interview_id){
		// go to interview, att end
		// initiate input
		alert('add an audio track to this interview');
	}
	views.deleteAudio = function(audio_id){
		// remove audio track
		alert('delete this audio track');
	}

	views.addQuote = function(audio_id, quoteText){
		// go to audio answer
		// focus on text field
		alert('add a quote to this audio track');
	}
	views.editQuote = function(quote_id){
		alert('edit this quote');
	}
	views.deleteQuote = function(quote_id){
		alert('delete this quote');
	}
   
	// photo views
	views.addInterviewPhoto = function(interview_id){
		// go to interview
		// add photo to interview
		alert('add a photo to this interview');
	}
	views.deletePhoto = function(photo_id){
		// remove photo
		alert('delete this photo');
	}
	 
	// location views
	views.addLocation = function(interview_id){
		// get gps location if possible.
		// go to map
		// if the interview already exists
			// just add the location to the map and highlight
		// if the interview does not exist
			// add the location and go to split view
		alert('add a location to this interview');
	}
	views.moveLocation = function(loc_id, latlon){
		// move the item
		alert('move the location of this interview');
	}
	views.deleteLocation = function(loc_id){
		// remove the location
		alert('delete this location');
	}

	return views;
}


// adjust size of buttons
$(".control-button g").attr("transform", "scale(0.8, 0.8)");
var views = Views();

