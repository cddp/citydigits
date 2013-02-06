
$('.delete-photo').click(function(e){
	// there is no delete photo button
	var photo_id = $(this).parents('.interview-photo-wrapper').attr('id');
	// delete the photo
	views.deletePhoto(photo_id);
});


$('.quote-delete').click(function(e){
	var quote_id = $(this).parents('.answer-quote').attr('id');
	// delete the quote
	views.deleteQuote(quote_id);
});

$('.record-button').click(function(e){
	var interview_id = $(this).parents('.interview').attr("id");
	var question_id = $(this).parents('.questionblock').attr("id");
	// add audio to question
	views.addAudioAnswer(interview_id, question_id);
});

$('.audio-delete').click(function(e){
	var audio_id = $(this).parents('.answer_audio').attr('id');
	// delete audio
	views.deleteAudio(audio_id);
});





