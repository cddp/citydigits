
$('.photo-input').click(function(e){
	var interview_id = $(this).parent('.interview').attr('id');
	// add a photo
	views.addInterviewPhoto(interview_id);
});

$('.delete-photo').click(function(e){
	var photo_id = $(this).parent('.photo').attr('id');
	// delete the photo
	views.deletePhoto(photo_id);
});

// add or edit quote
$('.quote-input').change(function(e){
	var val = $(this).val();
	if ($(this).hasClass('new')){
		var audio_id = $(this).parent('.audio').attr('id');
		// add a quote
		views.addQuote(audio_id, quoteText);
	} else {
		var quote_id = $(this).attr('id');
		// edit the quote
		views.editQuote(quote_id, quoteText);
	}
});


$('.quote-delete').click(function(e){
	// delete the quote
	views.deleteQuote(quote_id);
});

$('.microphone').click(function(e){
	// add audio to question
	views.addAudioAnswer(interview_id, question_id);
});

$('.audio-delete').click(function(e){
	// delete audio
	views.deleteAudio(audio_id);
});





